"use client";

import type { StruggleAlert as StruggleAlertType } from "@/types";
import { Card, CardContent } from "@/components/ui/Card";

export function StruggleAlertCard({ alert }: { alert: StruggleAlertType }) {
  const isHighConfidence = alert.confidence >= 0.8;
  return (
    <Card className={`border-l-4 ${isHighConfidence ? "border-l-red-500 bg-red-50" : "border-l-yellow-500 bg-yellow-50"}`}>
      <CardContent className="py-3">
        <div className="flex items-start justify-between">
          <div>
            <p className="font-medium text-gray-900">{alert.student_name}</p>
            <p className="text-sm text-gray-600 mt-0.5">{alert.struggle_type}{alert.details ? `: ${alert.details}` : ""}</p>
          </div>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${isHighConfidence ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700"}`}>
            {Math.round(alert.confidence * 100)}%
          </span>
        </div>
        <p className="text-xs text-gray-400 mt-1">{new Date(alert.timestamp).toLocaleString()}</p>
      </CardContent>
    </Card>
  );
}
