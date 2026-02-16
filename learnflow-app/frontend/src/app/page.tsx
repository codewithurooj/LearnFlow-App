"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/auth";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Loading } from "@/components/ui/Loading";

export default function Home() {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && session?.user) {
      router.push("/dashboard");
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loading />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="max-w-2xl text-center space-y-8">
        <h1 className="text-5xl font-bold text-gray-900">
          <span className="text-blue-600">LearnFlow</span>
        </h1>
        <p className="text-xl text-gray-600">
          AI-Powered Python Tutoring Platform
        </p>
        <p className="text-gray-500">
          Chat with AI tutors, write and run code, practice with exercises, and
          track your progress — all in one place.
        </p>

        <div className="flex gap-4 justify-center">
          <Link href="/auth/signup">
            <Button size="lg">Get Started</Button>
          </Link>
          <Link href="/auth/login">
            <Button variant="outline" size="lg">
              Sign In
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8">
          {[
            { icon: "💬", label: "AI Tutors" },
            { icon: "💻", label: "Code Editor" },
            { icon: "🏋️", label: "Exercises" },
            { icon: "📊", label: "Progress" },
          ].map((feature) => (
            <div
              key={feature.label}
              className="p-4 bg-white rounded-lg shadow-sm border border-gray-100"
            >
              <div className="text-2xl mb-2">{feature.icon}</div>
              <div className="text-sm font-medium text-gray-700">
                {feature.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
