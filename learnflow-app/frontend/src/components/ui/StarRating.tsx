import { cn } from "@/lib/utils";

interface StarRatingProps { rating: number; max?: number; size?: "sm" | "md" | "lg"; }

export function StarRating({ rating, max = 5, size = "md" }: StarRatingProps) {
  const sizeClasses = { sm: "text-sm", md: "text-lg", lg: "text-2xl" };
  return (
    <div className={cn("flex gap-0.5", sizeClasses[size])}>
      {Array.from({ length: max }, (_, i) => (
        <span key={i} className={i < rating ? "text-yellow-400" : "text-gray-300"}>★</span>
      ))}
    </div>
  );
}
