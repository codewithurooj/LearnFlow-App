import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const publicPaths = ["/auth/login", "/auth/signup", "/api/auth", "/api/health"];

function isPublicPath(pathname: string): boolean {
  return publicPaths.some((p) => pathname.startsWith(p));
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (isPublicPath(pathname)) {
    return NextResponse.next();
  }

  const sessionToken = request.cookies.get("better-auth.session_token")?.value;

  if (!sessionToken && pathname !== "/") {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
