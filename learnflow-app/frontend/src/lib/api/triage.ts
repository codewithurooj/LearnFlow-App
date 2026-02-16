import { triageClient } from "@/lib/api";
import type { TriageRequest, TriageResponse } from "@/types";

export const triageApi = {
  route: (data: TriageRequest) => triageClient.post<TriageResponse>("/api/v1/triage/route", data),
};
