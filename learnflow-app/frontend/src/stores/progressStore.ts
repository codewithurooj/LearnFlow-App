import { create } from "zustand";
import type { ProgressSummary, TopicMastery, TopicDetail } from "@/types";

interface ProgressState {
  summary: ProgressSummary | null;
  topics: TopicMastery[];
  selectedTopicDetail: TopicDetail | null;
  isLoading: boolean;
  isLoadingDetail: boolean;
  setSummary: (summary: ProgressSummary | null) => void;
  setTopics: (topics: TopicMastery[]) => void;
  setSelectedTopicDetail: (detail: TopicDetail | null) => void;
  setLoading: (loading: boolean) => void;
  setLoadingDetail: (loading: boolean) => void;
}

export const useProgressStore = create<ProgressState>((set) => ({
  summary: null, topics: [], selectedTopicDetail: null,
  isLoading: false, isLoadingDetail: false,
  setSummary: (summary) => set({ summary }),
  setTopics: (topics) => set({ topics }),
  setSelectedTopicDetail: (selectedTopicDetail) => set({ selectedTopicDetail }),
  setLoading: (isLoading) => set({ isLoading }),
  setLoadingDetail: (isLoadingDetail) => set({ isLoadingDetail }),
}));
