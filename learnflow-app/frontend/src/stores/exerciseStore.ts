import { create } from "zustand";
import type { Exercise, ExerciseResult } from "@/types";

interface ExerciseState {
  exercise: Exercise | null;
  result: ExerciseResult | null;
  topics: Record<string, string[]>;
  isGenerating: boolean;
  isSubmitting: boolean;
  setExercise: (exercise: Exercise | null) => void;
  setResult: (result: ExerciseResult | null) => void;
  setTopics: (topics: Record<string, string[]>) => void;
  setGenerating: (generating: boolean) => void;
  setSubmitting: (submitting: boolean) => void;
  reset: () => void;
}

export const useExerciseStore = create<ExerciseState>((set) => ({
  exercise: null, result: null, topics: {},
  isGenerating: false, isSubmitting: false,
  setExercise: (exercise) => set({ exercise, result: null }),
  setResult: (result) => set({ result }),
  setTopics: (topics) => set({ topics }),
  setGenerating: (isGenerating) => set({ isGenerating }),
  setSubmitting: (isSubmitting) => set({ isSubmitting }),
  reset: () => set({ exercise: null, result: null, isGenerating: false, isSubmitting: false }),
}));
