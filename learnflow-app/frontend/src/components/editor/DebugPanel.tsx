"use client";

import { useState } from "react";
import type { DebugResult } from "@/types";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";

interface DebugPanelProps { result: DebugResult | null; isLoading: boolean; onRequestSolution?: () => void; solutionCode?: string; }

export function DebugPanel({ result, isLoading, onRequestSolution, solutionCode }: DebugPanelProps) {
  const [showSolution, setShowSolution] = useState(false);

  if (isLoading) return <Card><CardContent className="flex items-center gap-2 text-gray-500"><div className="h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />Analyzing error...</CardContent></Card>;
  if (!result) return null;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">Debug Help</h3>
          <span className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded-full font-medium">{result.error_type}</span>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {result.error_line && <p className="text-sm text-gray-600">Error on <span className="font-mono font-medium text-red-600">line {result.error_line}</span></p>}
        <div><h4 className="text-sm font-medium text-gray-700 mb-1">Root Cause</h4><p className="text-sm text-gray-600">{result.root_cause}</p></div>
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
          <h4 className="text-sm font-medium text-yellow-800 mb-1">Hint</h4>
          <p className="text-sm text-yellow-700">{result.hint}</p>
        </div>
        {!showSolution && !solutionCode && (
          <Button variant="outline" size="sm" onClick={() => { onRequestSolution?.(); setShowSolution(true); }}>Show Solution</Button>
        )}
        {showSolution && result.solution && <div className="bg-green-50 border border-green-200 rounded-md p-3"><h4 className="text-sm font-medium text-green-800 mb-1">Solution</h4><p className="text-sm text-green-700">{result.solution}</p></div>}
        {solutionCode && <div><h4 className="text-sm font-medium text-green-800 mb-1">Corrected Code</h4><pre className="bg-gray-900 text-green-400 rounded-md p-3 text-sm overflow-x-auto">{solutionCode}</pre></div>}
      </CardContent>
    </Card>
  );
}
