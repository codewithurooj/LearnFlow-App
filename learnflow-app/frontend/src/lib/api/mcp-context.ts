import { mcpContextClient } from "@/lib/api";
import type { ClassOverview } from "@/types";

export const mcpContextApi = {
  classOverview: () => mcpContextClient.get<ClassOverview>("/api/v1/context/class/overview"),
  studentStruggles: (studentId: string) => mcpContextClient.get<{ struggles: unknown[]; patterns: unknown[] }>(`/api/v1/context/student/${studentId}/struggles`),
};
