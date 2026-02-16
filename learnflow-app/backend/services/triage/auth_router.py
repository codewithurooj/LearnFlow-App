"""
Better Auth-compatible authentication endpoints.

Implements sign-up, sign-in, get-session, and sign-out
to match the Better Auth client protocol used by the frontend.
"""

import os
import uuid
from datetime import datetime, timedelta, timezone

import asyncpg
import bcrypt
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

auth_router = APIRouter(prefix="/api/auth")

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://learnflow:learnflow_dev@localhost:5432/learnflow",
)

COOKIE_NAME = "better-auth.session_token"
SESSION_DURATION_DAYS = 7

# Connection pool (lazy init)
_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    return _pool


async def close_pool():
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


# ---------- Request models ----------

class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str


class SignInRequest(BaseModel):
    email: str
    password: str


# ---------- Helpers ----------

def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def _set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # localhost dev
        path="/",
        max_age=SESSION_DURATION_DAYS * 86400,
    )


def _clear_session_cookie(response: Response):
    response.delete_cookie(key=COOKIE_NAME, path="/")


def _user_dict(row: asyncpg.Record) -> dict:
    return {
        "id": str(row["id"]),
        "email": row["email"],
        "name": row["name"],
        "role": row["role"],
        "createdAt": row["created_at"].isoformat(),
        "updatedAt": row["updated_at"].isoformat(),
    }


# ---------- Endpoints ----------

@auth_router.post("/sign-up/email")
async def sign_up(body: SignUpRequest, response: Response):
    pool = await get_pool()

    # Check if user exists
    existing = await pool.fetchrow(
        "SELECT id FROM users WHERE email = $1", body.email
    )
    if existing:
        response.status_code = 400
        return {"error": "User already exists"}

    # Create user
    password_hash = _hash_password(body.password)
    user = await pool.fetchrow(
        """
        INSERT INTO users (email, name, password_hash, role)
        VALUES ($1, $2, $3, 'student')
        RETURNING id, email, name, role, created_at, updated_at
        """,
        body.email,
        body.name,
        password_hash,
    )

    # Create session
    token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=SESSION_DURATION_DAYS)
    await pool.execute(
        """
        INSERT INTO sessions (user_id, token, expires_at)
        VALUES ($1, $2, $3)
        """,
        user["id"],
        token,
        expires_at,
    )

    _set_session_cookie(response, token)

    return {
        "user": _user_dict(user),
        "session": {
            "token": token,
            "expiresAt": expires_at.isoformat(),
        },
    }


@auth_router.post("/sign-in/email")
async def sign_in(body: SignInRequest, response: Response):
    pool = await get_pool()

    user = await pool.fetchrow(
        """
        SELECT id, email, name, role, password_hash, created_at, updated_at
        FROM users WHERE email = $1
        """,
        body.email,
    )

    if not user or not _verify_password(body.password, user["password_hash"]):
        response.status_code = 401
        return {"error": "Invalid email or password"}

    # Create session
    token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=SESSION_DURATION_DAYS)
    await pool.execute(
        """
        INSERT INTO sessions (user_id, token, expires_at)
        VALUES ($1, $2, $3)
        """,
        user["id"],
        token,
        expires_at,
    )

    _set_session_cookie(response, token)

    return {
        "user": _user_dict(user),
        "session": {
            "token": token,
            "expiresAt": expires_at.isoformat(),
        },
    }


@auth_router.get("/get-session")
async def get_session(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return {"session": None, "user": None}

    pool = await get_pool()

    row = await pool.fetchrow(
        """
        SELECT s.token, s.expires_at,
               u.id, u.email, u.name, u.role, u.created_at, u.updated_at
        FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.token = $1 AND s.expires_at > NOW()
        """,
        token,
    )

    if not row:
        return {"session": None, "user": None}

    return {
        "session": {
            "token": row["token"],
            "expiresAt": row["expires_at"].isoformat(),
        },
        "user": _user_dict(row),
    }


@auth_router.post("/sign-out")
async def sign_out(request: Request, response: Response):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        pool = await get_pool()
        await pool.execute("DELETE FROM sessions WHERE token = $1", token)

    _clear_session_cookie(response)
    return {"success": True}
