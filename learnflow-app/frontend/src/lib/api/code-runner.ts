import { codeRunnerClient } from "@/lib/api";
import type { CodeExecutionRequest, CodeExecutionResult } from "@/types";

export const codeRunnerApi = {
  execute: (data: CodeExecutionRequest) => codeRunnerClient.post<CodeExecutionResult>("/api/v1/code/execute", data),
};
