import { progressClient } from "@/lib/api";
import type { ProgressSummary, TopicDetail } from "@/types";

export const progressApi = {
  getSummary: (studentId: string) => progressClient.get<ProgressSummary>(`/api/v1/progress/${studentId}`),
  getTopicDetail: (studentId: string, topicId: string) => progressClient.get<TopicDetail>(`/api/v1/progress/${studentId}/topic/${topicId}`),
};
