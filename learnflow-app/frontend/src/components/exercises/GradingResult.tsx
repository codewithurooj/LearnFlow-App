"use client";

import ReactMarkdown from "react-markdown";
import { Card, CardHeader, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import type { ExerciseResult } from "@/types";

export function GradingResult({ result, onTryAgain, onNewExercise }: { result: ExerciseResult; onTryAgain: () => void; onNewExercise: () => void }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">Results</h3>
          <span className={`text-sm font-medium px-3 py-1 rounded-full ${result.passed ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
            {result.passed ? "Passed" : "Not Passed"}
          </span>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1"><span className="font-medium text-gray-700">Score</span><span>{Math.round(result.score * 100)}%</span></div>
          <div className="w-full bg-gray-200 rounded-full h-2"><div className={`h-2 rounded-full ${result.passed ? "bg-green-500" : "bg-red-500"}`} style={{ width: `${result.score * 100}%` }} /></div>
        </div>
        {result.test_results.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Test Cases</h4>
            <ul className="space-y-1">{result.test_results.map((t, i) => (
              <li key={i} className="flex items-center gap-2 text-sm">
                <span className={t.passed ? "text-green-500" : "text-red-500"}>{t.passed ? "✓" : "✗"}</span>
                <span className="text-gray-700">{t.name}</span>
              </li>
            ))}</ul>
          </div>
        )}
        <div className="prose prose-sm max-w-none text-gray-700"><ReactMarkdown>{result.feedback}</ReactMarkdown></div>
        <div className="flex gap-2">
          {!result.passed && <Button variant="outline" onClick={onTryAgain}>Try Again</Button>}
          <Button onClick={onNewExercise}>New Exercise</Button>
        </div>
      </CardContent>
    </Card>
  );
}
