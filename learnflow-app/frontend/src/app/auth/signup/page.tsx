import { SignupForm } from "@/components/auth/SignupForm";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 -mt-14">
      <div className="max-w-md w-full space-y-6 p-8 bg-white rounded-lg shadow-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-blue-600">LearnFlow</h1>
          <p className="mt-2 text-gray-600">Create your account to start learning Python</p>
        </div>
        <SignupForm />
      </div>
    </div>
  );
}
