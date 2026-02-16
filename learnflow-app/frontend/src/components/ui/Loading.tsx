import { cn } from "@/lib/utils";

interface LoadingProps { className?: string; text?: string; }

export function Loading({ className, text = "Loading..." }: LoadingProps) {
  return (
    <div className={cn("flex items-center justify-center gap-2 text-gray-500", className)}>
      <div className="h-5 w-5 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />
      <span className="text-sm">{text}</span>
    </div>
  );
}
