"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { signUp } from "@/lib/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function SignupForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (password !== confirmPassword) { setError("Passwords do not match."); return; }
    if (password.length < 8) { setError("Password must be at least 8 characters."); return; }
    setIsLoading(true);
    try {
      await signUp.email({ name, email, password });
      router.push("/dashboard");
    } catch {
      setError("Failed to create account. Email may already be in use.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input id="name" label="Name" type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" required disabled={isLoading} />
      <Input id="email" label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required disabled={isLoading} />
      <Input id="password" label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required minLength={8} disabled={isLoading} />
      <Input id="confirm-password" label="Confirm Password" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="••••••••" required disabled={isLoading} />
      {error && <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">{error}</div>}
      <Button type="submit" className="w-full" disabled={isLoading}>{isLoading ? "Creating account..." : "Sign Up"}</Button>
      <p className="text-center text-sm text-gray-600">Already have an account?{" "}<Link href="/auth/login" className="text-blue-600 hover:underline">Sign in</Link></p>
    </form>
  );
}
