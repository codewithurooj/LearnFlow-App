"""
MCP Context Server API Routes

Exposes context endpoints that AI agents can query to get
real-time data for debugging, monitoring, and system expansion.
"""

from fastapi import APIRouter, Request, Query

router = APIRouter(tags=["context"])


@router.get("/student/{student_id}/progress")
async def get_student_progress(student_id: str, request: Request):
    """Get a student's progress and mastery data."""
    provider = request.app.state.context_provider
    return await provider.get_student_progress(student_id)


@router.get("/student/{student_id}/struggles")
async def get_student_struggles(student_id: str, request: Request):
    """Get a student's struggle history and patterns."""
    provider = request.app.state.context_provider
    return await provider.get_student_struggles(student_id)


@router.get("/student/{student_id}/submissions")
async def get_recent_submissions(
    student_id: str,
    request: Request,
    limit: int = Query(default=10, le=50),
):
    """Get a student's recent code submissions."""
    provider = request.app.state.context_provider
    return await provider.get_recent_submissions(student_id, limit=limit)


@router.get("/class/overview")
async def get_class_overview(request: Request):
    """Get aggregated class progress and struggle data."""
    provider = request.app.state.context_provider
    return await provider.get_class_overview()


@router.get("/system")
async def get_system_context(request: Request):
    """Get full system context including service health and configuration."""
    provider = request.app.state.context_provider
    return await provider.get_system_context()


@router.get("/system/health")
async def get_service_health(request: Request):
    """Check health status of all LearnFlow microservices."""
    provider = request.app.state.context_provider
    return await provider.get_service_health()
