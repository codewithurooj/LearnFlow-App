import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getMasteryColor(level: string): string {
  switch (level) {
    case "Beginner": return "#ef4444";
    case "Learning": return "#eab308";
    case "Proficient": return "#22c55e";
    case "Mastered": return "#3b82f6";
    default: return "#6b7280";
  }
}

export function getMasteryLevel(score: number): string {
  if (score <= 40) return "Beginner";
  if (score <= 70) return "Learning";
  if (score <= 90) return "Proficient";
  return "Mastered";
}
