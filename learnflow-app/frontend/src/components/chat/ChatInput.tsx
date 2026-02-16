"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";

export function ChatInput({ onSend, disabled }: { onSend: (msg: string) => void; disabled?: boolean }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <textarea
        value={input} onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } }}
        placeholder="Ask a Python question..." disabled={disabled} rows={1}
        className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      />
      <Button type="submit" disabled={disabled || !input.trim()}>Send</Button>
    </form>
  );
}
