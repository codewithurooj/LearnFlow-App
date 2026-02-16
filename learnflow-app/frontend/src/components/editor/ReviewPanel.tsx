"use client";

import type { CodeReviewResult } from "@/types";
import { StarRating } from "@/components/ui/StarRating";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";

function CriterionRow({ name, score, feedback }: { name: string; score: number; feedback: string }) {
  return (
    <div className="flex items-start gap-3 py-2">
      <div className="w-28 shrink-0"><span className="text-sm font-medium text-gray-700">{name}</span></div>
      <StarRating rating={score} size="sm" />
      <p className="text-sm text-gray-600 flex-1">{feedback}</p>
    </div>
  );
}

export function ReviewPanel({ result, isLoading }: { result: CodeReviewResult | null; isLoading: boolean }) {
  if (isLoading) return <Card><CardContent className="flex items-center gap-2 text-gray-500"><div className="h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />Reviewing...</CardContent></Card>;
  if (!result) return null;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">Code Review</h3>
          <div className="flex items-center gap-2"><StarRating rating={result.rating} size="md" /><span className="text-sm text-gray-500">{result.rating}/5</span></div>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="divide-y divide-gray-100">
          <CriterionRow name="Correctness" score={result.correctness.score} feedback={result.correctness.feedback} />
          <CriterionRow name="Style (PEP 8)" score={result.style.score} feedback={result.style.feedback} />
          <CriterionRow name="Efficiency" score={result.efficiency.score} feedback={result.efficiency.feedback} />
          <CriterionRow name="Readability" score={result.readability.score} feedback={result.readability.feedback} />
        </div>
        {result.strengths.length > 0 && <div><h4 className="text-sm font-medium text-green-700 mb-1">Strengths</h4><ul className="list-disc list-inside text-sm text-gray-600 space-y-1">{result.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul></div>}
        {result.suggestions.length > 0 && <div><h4 className="text-sm font-medium text-blue-700 mb-1">Suggestions</h4><ul className="list-disc list-inside text-sm text-gray-600 space-y-1">{result.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul></div>}
        {result.encouragement && <p className="text-sm text-purple-700 italic">{result.encouragement}</p>}
      </CardContent>
    </Card>
  );
}
