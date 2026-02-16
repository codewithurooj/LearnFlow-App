"use client";

import type { TopicMastery } from "@/types";
import { getMasteryColor } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/Card";

export function TopicCard({ topic, onClick }: { topic: TopicMastery; onClick: () => void }) {
  const color = getMasteryColor(topic.mastery_level);
  return (
    <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={onClick}>
      <CardContent className="py-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-medium text-gray-900">{topic.topic_name}</h3>
          <span className="text-xs font-medium px-2 py-0.5 rounded-full" style={{ backgroundColor: `${color}20`, color }}>{topic.mastery_level}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div className="h-2 rounded-full transition-all" style={{ width: `${topic.mastery_score}%`, backgroundColor: color }} />
        </div>
        <p className="text-xs text-gray-500 mt-1">{Math.round(topic.mastery_score)}%</p>
      </CardContent>
    </Card>
  );
}
