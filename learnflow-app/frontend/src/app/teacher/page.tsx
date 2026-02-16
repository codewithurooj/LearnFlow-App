"use client";

import { useEffect, useState, useCallback } from "react";
import { mcpContextApi } from "@/lib/api/mcp-context";
import { ClassOverview } from "@/components/teacher/ClassOverview";
import { StruggleAlertCard } from "@/components/teacher/StruggleAlert";
import { Loading } from "@/components/ui/Loading";
import type { ClassOverview as ClassOverviewType } from "@/types";

export default function TeacherPage() {
  const [overview, setOverview] = useState<ClassOverviewType | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const ov = await mcpContextApi.classOverview();
      setOverview(ov);
    } catch {} finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  // Poll for updates every 30 seconds
  useEffect(() => {
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  if (loading) return <Loading text="Loading teacher dashboard..." />;

  return (
    <div className="max-w-6xl mx-auto py-6 px-4 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Teacher Dashboard</h1>
      {overview && <ClassOverview data={overview} />}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Recent Struggle Alerts</h2>
        <div className="space-y-2">
          {overview?.recent_struggles.map((a, i) => <StruggleAlertCard key={i} alert={a} />)}
          {(!overview || overview.recent_struggles.length === 0) && <p className="text-sm text-gray-500">No active struggle alerts.</p>}
        </div>
      </div>
    </div>
  );
}
