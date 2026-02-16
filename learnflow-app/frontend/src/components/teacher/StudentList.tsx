"use client";

import { useState } from "react";
import { getMasteryColor } from "@/lib/utils";
import { Card, CardHeader, CardContent } from "@/components/ui/Card";

interface StudentRow {
  student_id: string;
  name: string;
  mastery: number;
  mastery_level: string;
  exercises_completed: number;
  last_active: string;
}

type SortKey = "name" | "mastery" | "exercises_completed" | "last_active";

export function StudentList({ students }: { students: StudentRow[] }) {
  const [sortKey, setSortKey] = useState<SortKey>("mastery");
  const [asc, setAsc] = useState(false);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) setAsc(!asc);
    else { setSortKey(key); setAsc(key === "name"); }
  };

  const sorted = [...students].sort((a, b) => {
    const dir = asc ? 1 : -1;
    if (sortKey === "name") return dir * a.name.localeCompare(b.name);
    if (sortKey === "mastery") return dir * (a.mastery - b.mastery);
    if (sortKey === "exercises_completed") return dir * (a.exercises_completed - b.exercises_completed);
    return dir * (new Date(a.last_active).getTime() - new Date(b.last_active).getTime());
  });

  const Header = ({ label, field }: { label: string; field: SortKey }) => (
    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase cursor-pointer hover:text-gray-700" onClick={() => handleSort(field)}>
      {label} {sortKey === field && (asc ? "↑" : "↓")}
    </th>
  );

  return (
    <Card>
      <CardHeader><h3 className="font-semibold text-gray-900">Students</h3></CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className="border-b">
            <Header label="Name" field="name" />
            <Header label="Mastery" field="mastery" />
            <Header label="Exercises" field="exercises_completed" />
            <Header label="Last Active" field="last_active" />
          </tr></thead>
          <tbody>
            {sorted.map((s) => {
              const color = getMasteryColor(s.mastery_level);
              return (
                <tr key={s.student_id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-900">{s.name}</td>
                  <td className="px-4 py-3">
                    <span className="text-xs font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: `${color}20`, color }}>{Math.round(s.mastery)}% — {s.mastery_level}</span>
                  </td>
                  <td className="px-4 py-3 text-gray-600">{s.exercises_completed}</td>
                  <td className="px-4 py-3 text-gray-500">{new Date(s.last_active).toLocaleDateString()}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {students.length === 0 && <p className="text-center text-sm text-gray-500 py-4">No students enrolled yet.</p>}
      </CardContent>
    </Card>
  );
}
