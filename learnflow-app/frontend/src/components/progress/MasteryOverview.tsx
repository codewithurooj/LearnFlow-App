"use client";

import type { ProgressSummary } from "@/types";
import { getMasteryColor } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/Card";

export function MasteryOverview({ summary }: { summary: ProgressSummary }) {
  const color = getMasteryColor(summary.overall_level);
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card><CardContent className="text-center py-6">
        <div className="relative inline-flex items-center justify-center w-24 h-24">
          <svg className="w-24 h-24 -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="42" fill="none" stroke="#e5e7eb" strokeWidth="8" />
            <circle cx="50" cy="50" r="42" fill="none" stroke={color} strokeWidth="8" strokeDasharray={`${summary.overall_mastery * 2.64} 264`} strokeLinecap="round" />
          </svg>
          <span className="absolute text-xl font-bold" style={{ color }}>{Math.round(summary.overall_mastery)}%</span>
        </div>
        <p className="mt-2 text-sm font-medium" style={{ color }}>{summary.overall_level}</p>
      </CardContent></Card>
      <Card><CardContent className="text-center py-6"><p className="text-3xl font-bold text-orange-500">{summary.current_streak}</p><p className="text-sm text-gray-500 mt-1">Day Streak</p></CardContent></Card>
      <Card><CardContent className="text-center py-6"><p className="text-3xl font-bold text-blue-600">{summary.total_exercises}</p><p className="text-sm text-gray-500 mt-1">Exercises</p></CardContent></Card>
      <Card><CardContent className="text-center py-6"><p className="text-3xl font-bold text-purple-600">{summary.total_quizzes}</p><p className="text-sm text-gray-500 mt-1">Quizzes</p></CardContent></Card>
    </div>
  );
}
