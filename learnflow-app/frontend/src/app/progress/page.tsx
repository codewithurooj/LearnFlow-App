"use client";

import { useEffect, useState } from "react";
import { useSession } from "@/lib/auth";
import { progressApi } from "@/lib/api/progress";
import { useProgressStore } from "@/stores/progressStore";
import { MasteryOverview } from "@/components/progress/MasteryOverview";
import { TopicCard } from "@/components/progress/TopicCard";
import { TopicDetail } from "@/components/progress/TopicDetail";
import { Loading } from "@/components/ui/Loading";
import type { TopicDetail as TopicDetailType } from "@/types";

export default function ProgressPage() {
  const { data: session } = useSession();
  const userId = (session?.user as { id?: string } | undefined)?.id || "";
  const { summary, setSummary } = useProgressStore();
  const [loading, setLoading] = useState(true);
  const [selectedDetail, setSelectedDetail] = useState<TopicDetailType | null>(null);

  useEffect(() => {
    if (!userId) return;
    progressApi.getSummary(userId)
      .then(setSummary)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [userId, setSummary]);

  const handleTopicClick = async (topicId: string) => {
    try {
      const detail = await progressApi.getTopicDetail(userId, topicId);
      setSelectedDetail(detail);
    } catch {}
  };

  if (loading) return <Loading text="Loading progress..." />;

  const topics = summary?.topics || [];

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">My Progress</h1>
      {summary && <MasteryOverview summary={summary} />}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Topics</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {topics.map((t) => (
            <TopicCard key={t.topic_id} topic={t} onClick={() => handleTopicClick(t.topic_id)} />
          ))}
        </div>
        {topics.length === 0 && <p className="text-sm text-gray-500">No topic data yet. Complete exercises and quizzes to see your progress.</p>}
      </div>
      {selectedDetail && <TopicDetail detail={selectedDetail} onClose={() => setSelectedDetail(null)} />}
    </div>
  );
}
