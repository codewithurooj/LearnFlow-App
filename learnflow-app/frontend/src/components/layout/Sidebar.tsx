"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSession } from "@/lib/auth";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: "🏠" },
  { href: "/learn", label: "Learn", icon: "💬" },
  { href: "/code", label: "Code", icon: "💻" },
  { href: "/exercises", label: "Exercises", icon: "🏋️" },
  { href: "/progress", label: "Progress", icon: "📊" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { data: session } = useSession();
  const user = session?.user as { role?: string } | undefined;

  return (
    <aside className="w-56 bg-white border-r border-gray-200 min-h-[calc(100vh-3.5rem)] p-4">
      <nav className="space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
              pathname === item.href
                ? "bg-blue-50 text-blue-700 font-medium"
                : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
            )}
          >
            <span>{item.icon}</span>
            {item.label}
          </Link>
        ))}

        {user?.role === "teacher" && (
          <Link
            href="/teacher"
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors mt-4 border-t pt-4",
              pathname === "/teacher"
                ? "bg-purple-50 text-purple-700 font-medium"
                : "text-purple-600 hover:bg-purple-50 hover:text-purple-900"
            )}
          >
            <span>👩‍🏫</span>
            Teacher
          </Link>
        )}
      </nav>
    </aside>
  );
}
