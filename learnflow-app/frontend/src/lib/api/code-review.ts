import { codeReviewClient } from "@/lib/api";
import type { ReviewRequest, CodeReviewResult } from "@/types";

export const codeReviewApi = {
  analyze: (data: ReviewRequest) => codeReviewClient.post<CodeReviewResult>("/api/v1/review/analyze", data),
};
