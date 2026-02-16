import { exerciseClient } from "@/lib/api";
import type { Exercise, ExerciseSubmission, ExerciseResult } from "@/types";

export const exerciseApi = {
  generate: (studentId: string, topic: string, difficulty?: string) => {
    const params = new URLSearchParams({ student_id: studentId, topic });
    if (difficulty) params.set("difficulty", difficulty);
    return exerciseClient.get<Exercise>(`/api/v1/exercises/generate?${params}`);
  },
  submit: (data: ExerciseSubmission) => exerciseClient.post<ExerciseResult>("/api/v1/exercises/submit", data),
  topics: () => exerciseClient.get<Record<string, string[]>>("/api/v1/exercises/topics"),
};
