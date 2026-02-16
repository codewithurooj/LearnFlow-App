"use client";

import type { TopicDetail as TopicDetailType } from "@/types";
import { getMasteryColor } from "@/lib/utils";
import { Card, CardHeader, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

function BreakdownBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm"><span className="text-gray-600">{label}</span><span className="font-medium">{Math.round(value)}%</span></div>
      <div className="w-full bg-gray-200 rounded-full h-2"><div className="h-2 rounded-full" style={{ width: `${value}%`, backgroundColor: color }} /></div>
    </div>
  );
}

export function TopicDetail({ detail, onClose }: { detail: TopicDetailType; onClose: () => void }) {
  const color = getMasteryColor(detail.mastery_level);
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-lg max-h-[80vh] overflow-y-auto">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div><h3 className="text-lg font-semibold text-gray-900">{detail.topic_name}</h3><p className="text-sm mt-1" style={{ color }}>{detail.mastery_level} — {Math.round(detail.mastery_score)}%</p></div>
            <Button variant="ghost" size="sm" onClick={onClose}>✕</Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-gray-700">Mastery Breakdown</h4>
            <BreakdownBar label="Exercises (40%)" value={detail.breakdown.exercises} color="#3b82f6" />
            <BreakdownBar label="Quizzes (30%)" value={detail.breakdown.quizzes} color="#8b5cf6" />
            <BreakdownBar label="Code Quality (20%)" value={detail.breakdown.code_quality} color="#22c55e" />
            <BreakdownBar label="Streak (10%)" value={detail.breakdown.streak} color="#f59e0b" />
          </div>
          {detail.improvement_suggestions.length > 0 && (
            <div><h4 className="text-sm font-medium text-gray-700 mb-2">Improvement Suggestions</h4>
            <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">{detail.improvement_suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul></div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
