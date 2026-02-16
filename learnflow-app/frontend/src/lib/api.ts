export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((options.headers as Record<string, string>) || {}),
  };

  const response = await fetch(url, { ...options, headers, credentials: "include" });

  if (!response.ok) {
    const errorBody = await response.text().catch(() => "Unknown error");
    throw new ApiError(response.status, errorBody);
  }

  return response.json();
}

export function createServiceClient(baseUrl: string) {
  return {
    get: <T>(path: string) => request<T>(`${baseUrl}${path}`),
    post: <T>(path: string, body: unknown) =>
      request<T>(`${baseUrl}${path}`, { method: "POST", body: JSON.stringify(body) }),
  };
}

const TRIAGE_URL = process.env.NEXT_PUBLIC_TRIAGE_URL || "http://localhost:8001";
const CONCEPTS_URL = process.env.NEXT_PUBLIC_CONCEPTS_URL || "http://localhost:8002";
const CODE_RUNNER_URL = process.env.NEXT_PUBLIC_CODE_RUNNER_URL || "http://localhost:8003";
const DEBUG_URL = process.env.NEXT_PUBLIC_DEBUG_URL || "http://localhost:8004";
const EXERCISE_URL = process.env.NEXT_PUBLIC_EXERCISE_URL || "http://localhost:8005";
const PROGRESS_URL = process.env.NEXT_PUBLIC_PROGRESS_URL || "http://localhost:8006";
const CODE_REVIEW_URL = process.env.NEXT_PUBLIC_CODE_REVIEW_URL || "http://localhost:8007";
const MCP_CONTEXT_URL = process.env.NEXT_PUBLIC_MCP_CONTEXT_URL || "http://localhost:8008";

export const triageClient = createServiceClient(TRIAGE_URL);
export const conceptsClient = createServiceClient(CONCEPTS_URL);
export const codeRunnerClient = createServiceClient(CODE_RUNNER_URL);
export const debugClient = createServiceClient(DEBUG_URL);
export const exerciseClient = createServiceClient(EXERCISE_URL);
export const progressClient = createServiceClient(PROGRESS_URL);
export const codeReviewClient = createServiceClient(CODE_REVIEW_URL);
export const mcpContextClient = createServiceClient(MCP_CONTEXT_URL);
