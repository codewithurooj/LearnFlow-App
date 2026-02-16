"use client";

import { useEffect, useState } from "react";
import { useSession } from "@/lib/auth";
import { useExerciseStore } from "@/stores/exerciseStore";
import { exerciseApi } from "@/lib/api/exercise";
import { TopicSelector } from "@/components/exercises/TopicSelector";
import { ExerciseCard } from "@/components/exercises/ExerciseCard";
import { GradingResult } from "@/components/exercises/GradingResult";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { Button } from "@/components/ui/Button";

export default function ExercisesPage() {
  const { data: session } = useSession();
  const userId = (session?.user as { id?: string } | undefined)?.id || "";
  const { exercise, result, topics, isGenerating, isSubmitting, setExercise, setResult, setTopics, setGenerating, setSubmitting, reset } = useExerciseStore();
  const [exerciseCode, setExerciseCode] = useState("");

  useEffect(() => { exerciseApi.topics().then(setTopics).catch(() => {}); }, [setTopics]);
  useEffect(() => { setExerciseCode(exercise?.starter_code || ""); }, [exercise]);

  const handleGenerate = async (topic: string, difficulty: string) => {
    setGenerating(true); setResult(null);
    try { setExercise(await exerciseApi.generate(userId, topic, difficulty)); } catch {} finally { setGenerating(false); }
  };

  const handleSubmit = async () => {
    if (!exercise) return;
    setSubmitting(true);
    try { setResult(await exerciseApi.submit({ student_id: userId, exercise_id: exercise.exercise_id, code: exerciseCode })); } catch {} finally { setSubmitting(false); }
  };

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Coding Exercises</h1>
      <TopicSelector topics={topics} onGenerate={handleGenerate} isLoading={isGenerating} />
      {exercise && (
        <div className="space-y-4">
          <ExerciseCard exercise={exercise} />
          <CodeEditor height="300px" defaultValue={exerciseCode} onChange={setExerciseCode} />
          <Button onClick={handleSubmit} disabled={isSubmitting || !exerciseCode.trim()}>{isSubmitting ? "Submitting..." : "Submit Solution"}</Button>
        </div>
      )}
      {result && <GradingResult result={result} onTryAgain={() => setResult(null)} onNewExercise={reset} />}
    </div>
  );
}
