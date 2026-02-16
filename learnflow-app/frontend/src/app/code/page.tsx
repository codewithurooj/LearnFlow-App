"use client";

import { useState } from "react";
import { useSession } from "@/lib/auth";
import { useEditorStore } from "@/stores/editorStore";
import { codeRunnerApi } from "@/lib/api/code-runner";
import { codeReviewApi } from "@/lib/api/code-review";
import { debugApi } from "@/lib/api/debug";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { OutputPanel } from "@/components/editor/OutputPanel";
import { ReviewPanel } from "@/components/editor/ReviewPanel";
import { DebugPanel } from "@/components/editor/DebugPanel";
import { Button } from "@/components/ui/Button";

export default function CodePage() {
  const { data: session } = useSession();
  const userId = (session?.user as { id?: string } | undefined)?.id || "";
  const { code, isRunning, setRunning, isReviewing, setReviewing, isDebugging, setDebugging, executionResult, setExecutionResult, reviewResult, setReviewResult, debugResult, setDebugResult } = useEditorStore();
  const [solutionCode, setSolutionCode] = useState<string | undefined>();

  const handleRun = async () => {
    setRunning(true); setExecutionResult(null); setReviewResult(null); setDebugResult(null); setSolutionCode(undefined);
    try {
      const result = await codeRunnerApi.execute({ student_id: userId, code });
      setExecutionResult(result);
    } catch {
      setExecutionResult({ stdout: "", stderr: "Failed to connect to code execution service.", exit_code: 1, execution_time_ms: 0, memory_used_mb: 0, timed_out: false, error_type: "ConnectionError" });
    } finally { setRunning(false); }
  };

  const handleReview = async () => {
    setReviewing(true); setReviewResult(null);
    try { setReviewResult(await codeReviewApi.analyze({ student_id: userId, code })); } catch {} finally { setReviewing(false); }
  };

  const handleGetHelp = async () => {
    if (!executionResult?.stderr) return;
    setDebugging(true); setDebugResult(null); setSolutionCode(undefined);
    try { setDebugResult(await debugApi.analyze({ student_id: userId, code, error_output: executionResult.stderr })); } catch {} finally { setDebugging(false); }
  };

  const handleRequestSolution = async () => {
    if (!executionResult?.stderr) return;
    try { const r = await debugApi.solution({ student_id: userId, code, error_output: executionResult.stderr }); setSolutionCode(r.corrected_code); } catch {}
  };

  return (
    <div className="max-w-6xl mx-auto py-6 px-4 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Code Editor</h1>
        <div className="flex gap-2">
          <Button onClick={handleRun} disabled={isRunning || !code.trim()}>{isRunning ? "Running..." : "Run Code"}</Button>
          <Button variant="outline" onClick={handleReview} disabled={isReviewing || !code.trim()}>{isReviewing ? "Reviewing..." : "Review Code"}</Button>
        </div>
      </div>
      <CodeEditor height="400px" />
      <OutputPanel result={executionResult} isRunning={isRunning} onGetHelp={handleGetHelp} />
      <ReviewPanel result={reviewResult} isLoading={isReviewing} />
      <DebugPanel result={debugResult} isLoading={isDebugging} onRequestSolution={handleRequestSolution} solutionCode={solutionCode} />
    </div>
  );
}
