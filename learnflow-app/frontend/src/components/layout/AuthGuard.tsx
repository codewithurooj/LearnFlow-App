"use client";

import { useSession } from "@/lib/auth";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";
import { Loading } from "@/components/ui/Loading";

const publicPaths = ["/auth/login", "/auth/signup", "/"];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const pathname = usePathname();
  const isPublicPath = publicPaths.includes(pathname);

  useEffect(() => {
    if (!isPending && !session?.user && !isPublicPath) {
      router.push("/auth/login");
    }
  }, [session, isPending, isPublicPath, router]);

  if (isPending) {
    return <div className="min-h-screen flex items-center justify-center"><Loading /></div>;
  }

  if (!session?.user && !isPublicPath) return null;

  return <>{children}</>;
}
