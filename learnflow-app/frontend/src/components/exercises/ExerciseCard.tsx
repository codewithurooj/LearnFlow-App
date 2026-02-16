"use client";

import ReactMarkdown from "react-markdown";
import { Card, CardHeader, CardContent } from "@/components/ui/Card";
import type { Exercise } from "@/types";

export function ExerciseCard({ exercise }: { exercise: Exercise }) {
  return (
    <Card>
      <CardHeader><h3 className="text-lg font-semibold text-gray-900">{exercise.title}</h3></CardHeader>
      <CardContent className="space-y-3">
        <div className="prose prose-sm max-w-none text-gray-700"><ReactMarkdown>{exercise.description}</ReactMarkdown></div>
        {exercise.expected_output_hint && (
          <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
            <p className="text-sm text-blue-700"><span className="font-medium">Expected output hint:</span> {exercise.expected_output_hint}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
