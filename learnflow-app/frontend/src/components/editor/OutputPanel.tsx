"use client";

import type { CodeExecutionResult } from "@/types";
import { Button } from "@/components/ui/Button";

interface OutputPanelProps { result: CodeExecutionResult | null; isRunning: boolean; onGetHelp?: () => void; }

export function OutputPanel({ result, isRunning, onGetHelp }: OutputPanelProps) {
  if (isRunning) {
    return (
      <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm text-gray-300">
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 animate-spin rounded-full border-2 border-gray-500 border-t-green-400" />
          Running code...
        </div>
      </div>
    );
  }

  if (!result) {
    return <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm text-gray-500">Output will appear here after running your code.</div>;
  }

  const hasError = result.stderr || result.error_type;
  const hasOutput = result.stdout.trim().length > 0;

  return (
    <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm space-y-2">
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>{result.timed_out ? "Timed out (5s limit)" : `Executed in ${result.execution_time_ms}ms`}</span>
        <span>{result.memory_used_mb.toFixed(1)}MB</span>
      </div>
      {result.timed_out && <div className="text-yellow-400">Your code exceeded the 5-second execution time limit.</div>}
      {hasOutput && <pre className="text-green-400 whitespace-pre-wrap">{result.stdout}</pre>}
      {!hasOutput && !hasError && !result.timed_out && <div className="text-gray-400">Program executed successfully with no output.</div>}
      {hasError && (
        <div className="space-y-2">
          <pre className="text-red-400 whitespace-pre-wrap">{result.stderr}</pre>
          {onGetHelp && <Button variant="outline" size="sm" onClick={onGetHelp} className="text-red-300 border-red-700 hover:bg-red-900/30">Get Help with this Error</Button>}
        </div>
      )}
    </div>
  );
}
