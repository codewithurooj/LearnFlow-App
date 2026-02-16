import { create } from "zustand";
import type { CodeExecutionResult, CodeReviewResult, DebugResult } from "@/types";

const STORAGE_KEY = "learnflow:code";
function loadSavedCode(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem(STORAGE_KEY) || "";
}

interface EditorState {
  code: string;
  isRunning: boolean;
  isReviewing: boolean;
  isDebugging: boolean;
  executionResult: CodeExecutionResult | null;
  reviewResult: CodeReviewResult | null;
  debugResult: DebugResult | null;
  setCode: (code: string) => void;
  setRunning: (running: boolean) => void;
  setReviewing: (reviewing: boolean) => void;
  setDebugging: (debugging: boolean) => void;
  setExecutionResult: (result: CodeExecutionResult | null) => void;
  setReviewResult: (result: CodeReviewResult | null) => void;
  setDebugResult: (result: DebugResult | null) => void;
  clearResults: () => void;
}

export const useEditorStore = create<EditorState>((set) => ({
  code: loadSavedCode(),
  isRunning: false, isReviewing: false, isDebugging: false,
  executionResult: null, reviewResult: null, debugResult: null,
  setCode: (code) => {
    if (typeof window !== "undefined") localStorage.setItem(STORAGE_KEY, code);
    set({ code });
  },
  setRunning: (isRunning) => set({ isRunning }),
  setReviewing: (isReviewing) => set({ isReviewing }),
  setDebugging: (isDebugging) => set({ isDebugging }),
  setExecutionResult: (executionResult) => set({ executionResult }),
  setReviewResult: (reviewResult) => set({ reviewResult }),
  setDebugResult: (debugResult) => set({ debugResult }),
  clearResults: () => set({ executionResult: null, reviewResult: null, debugResult: null }),
}));
