"use client";

import { useRef, useEffect } from "react";
import { useSession } from "@/lib/auth";
import { useChatStore } from "@/stores/chatStore";
import { triageApi } from "@/lib/api/triage";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ErrorMessage } from "@/components/ui/ErrorMessage";

export function ChatInterface() {
  const { data: session } = useSession();
  const userId = (session?.user as { id?: string } | undefined)?.id || "";
  const { messages, isLoading, error, addMessage, setLoading, setError } = useChatStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => { scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" }); }, [messages]);

  const handleSend = async (question: string) => {
    addMessage({ id: crypto.randomUUID(), role: "user", content: question, timestamp: new Date().toISOString() });
    setLoading(true); setError(null);
    try {
      const response = await triageApi.route({ student_id: userId, question });
      addMessage({ id: crypto.randomUUID(), role: "assistant", content: response.response, relatedTopics: response.sources, timestamp: new Date().toISOString() });
    } catch { setError("Failed to get a response. Please try again."); }
    finally { setLoading(false); }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg font-medium">Ask me anything about Python!</p>
            <p className="text-sm mt-1">Try: &quot;How do list comprehensions work?&quot;</p>
          </div>
        )}
        {messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 text-sm text-gray-500 flex items-center gap-2">
              <div className="h-3 w-3 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />Thinking...
            </div>
          </div>
        )}
        {error && <ErrorMessage message={error} onRetry={() => setError(null)} />}
      </div>
      <div className="border-t bg-white p-4"><ChatInput onSend={handleSend} disabled={isLoading} /></div>
    </div>
  );
}
