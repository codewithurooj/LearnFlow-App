"use client";

import { useSession } from "@/lib/auth";
import { Card, CardContent } from "@/components/ui/Card";
import Link from "next/link";

const features = [
  {
    title: "Learn",
    description: "Chat with AI tutors to learn Python concepts",
    href: "/learn",
    icon: "💬",
    color: "bg-blue-50 hover:bg-blue-100",
  },
  {
    title: "Code",
    description: "Write and run Python code in the editor",
    href: "/code",
    icon: "💻",
    color: "bg-green-50 hover:bg-green-100",
  },
  {
    title: "Exercises",
    description: "Practice with auto-graded coding challenges",
    href: "/exercises",
    icon: "🏋️",
    color: "bg-purple-50 hover:bg-purple-100",
  },
  {
    title: "Progress",
    description: "Track your mastery across Python topics",
    href: "/progress",
    icon: "📊",
    color: "bg-orange-50 hover:bg-orange-100",
  },
];

export default function DashboardPage() {
  const { data: session } = useSession();
  const user = session?.user as { name?: string; email?: string } | undefined;

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.name || "Student"}!
        </h1>
        <p className="text-gray-500 mt-1">What would you like to learn today?</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {features.map((feature) => (
          <Link key={feature.href} href={feature.href}>
            <Card className={`${feature.color} transition-colors cursor-pointer h-full`}>
              <CardContent className="py-6">
                <div className="text-3xl mb-3">{feature.icon}</div>
                <h2 className="text-lg font-semibold text-gray-900">{feature.title}</h2>
                <p className="text-sm text-gray-600 mt-1">{feature.description}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
