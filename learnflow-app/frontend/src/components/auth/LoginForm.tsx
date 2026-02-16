"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { signIn } from "@/lib/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      await signIn.email({ email, password });
      router.push("/dashboard");
    } catch {
      setError("Invalid email or password.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input id="email" label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required disabled={isLoading} />
      <Input id="password" label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required disabled={isLoading} />
      {error && <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">{error}</div>}
      <Button type="submit" className="w-full" disabled={isLoading}>{isLoading ? "Signing in..." : "Sign In"}</Button>
      <p className="text-center text-sm text-gray-600">Don&apos;t have an account?{" "}<Link href="/auth/signup" className="text-blue-600 hover:underline">Sign up</Link></p>
    </form>
  );
}
