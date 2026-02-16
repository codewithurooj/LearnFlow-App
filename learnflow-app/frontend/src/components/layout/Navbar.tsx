"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth";
import { Button } from "@/components/ui/Button";

export function Navbar() {
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const handleSignOut = async () => { await signOut(); router.push("/auth/login"); };
  const user = session?.user as { name?: string; email?: string; role?: string } | undefined;

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/dashboard" className="text-xl font-bold text-blue-600">LearnFlow</Link>
        {!isPending && user && (
          <div className="flex items-center gap-4">
            <nav className="hidden md:flex items-center gap-1">
              {[
                { href: "/dashboard", label: "Dashboard" },
                { href: "/learn", label: "Learn" },
                { href: "/code", label: "Code" },
                { href: "/exercises", label: "Exercises" },
                { href: "/progress", label: "Progress" },
              ].map((item) => (
                <Link key={item.href} href={item.href} className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100">
                  {item.label}
                </Link>
              ))}
              {user.role === "teacher" && (
                <Link href="/teacher" className="px-3 py-2 text-sm text-purple-600 hover:text-purple-900 rounded-md hover:bg-purple-50">Teacher</Link>
              )}
            </nav>
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-600">{user.name || user.email}</span>
              <Button variant="outline" size="sm" onClick={handleSignOut}>Sign Out</Button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
