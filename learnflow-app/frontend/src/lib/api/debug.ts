import { debugClient } from "@/lib/api";
import type { DebugRequest, DebugResult } from "@/types";

export const debugApi = {
  analyze: (data: DebugRequest) => debugClient.post<DebugResult>("/api/v1/debug/analyze", data),
  solution: (data: DebugRequest) => debugClient.post<{ solution: string; corrected_code: string }>("/api/v1/debug/solution", data),
};
