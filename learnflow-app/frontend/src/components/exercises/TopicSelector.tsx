"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";

export function TopicSelector({ topics, onGenerate, isLoading }: { topics: Record<string, string[]>; onGenerate: (topic: string, difficulty: string) => void; isLoading: boolean }) {
  const [selectedDifficulty, setSelectedDifficulty] = useState("");
  const [selectedTopic, setSelectedTopic] = useState("");
  const difficulties = Object.keys(topics);
  const availableTopics = selectedDifficulty ? topics[selectedDifficulty] || [] : [];

  return (
    <div className="flex flex-wrap items-end gap-3">
      <div className="space-y-1">
        <label className="text-sm font-medium text-gray-700">Difficulty</label>
        <select value={selectedDifficulty} onChange={(e) => { setSelectedDifficulty(e.target.value); setSelectedTopic(""); }} className="block rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500">
          <option value="">Select difficulty</option>
          {difficulties.map((d) => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
        </select>
      </div>
      <div className="space-y-1">
        <label className="text-sm font-medium text-gray-700">Topic</label>
        <select value={selectedTopic} onChange={(e) => setSelectedTopic(e.target.value)} disabled={!selectedDifficulty} className="block rounded-md border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 disabled:opacity-50">
          <option value="">Select topic</option>
          {availableTopics.map((t) => <option key={t} value={t}>{t.replace(/_/g, " ")}</option>)}
        </select>
      </div>
      <Button onClick={() => onGenerate(selectedTopic, selectedDifficulty)} disabled={!selectedTopic || isLoading}>{isLoading ? "Generating..." : "Generate Exercise"}</Button>
    </div>
  );
}
