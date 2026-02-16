"use client";

import type { ClassOverview as ClassOverviewType } from "@/types";
import { Card, CardContent } from "@/components/ui/Card";
import { getMasteryColor } from "@/lib/utils";

export function ClassOverview({ data }: { data: ClassOverviewType }) {
  const color = getMasteryColor(data.average_mastery >= 91 ? "Mastered" : data.average_mastery >= 71 ? "Proficient" : data.average_mastery >= 41 ? "Learning" : "Beginner");
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card><CardContent className="text-center py-6">
        <p className="text-3xl font-bold" style={{ color }}>{Math.round(data.average_mastery)}%</p>
        <p className="text-sm text-gray-500 mt-1">Class Average</p>
      </CardContent></Card>
      <Card><CardContent className="text-center py-6">
        <p className="text-3xl font-bold text-blue-600">{data.total_students}</p>
        <p className="text-sm text-gray-500 mt-1">Students</p>
      </CardContent></Card>
      <Card><CardContent className="text-center py-6">
        <p className="text-3xl font-bold text-purple-600">{data.active_students}</p>
        <p className="text-sm text-gray-500 mt-1">Active</p>
      </CardContent></Card>
      <Card><CardContent className="text-center py-6">
        <p className="text-3xl font-bold text-red-500">{data.recent_struggles.length}</p>
        <p className="text-sm text-gray-500 mt-1">Struggles</p>
      </CardContent></Card>
    </div>
  );
}
