"use client";

import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import type { ChatMessage as ChatMessageType } from "@/types";
import { cn } from "@/lib/utils";

export function ChatMessage({ message }: { message: ChatMessageType }) {
  const isUser = message.role === "user";
  return (
    <div className={cn("flex gap-3", isUser ? "justify-end" : "justify-start")}>
      <div className={cn("max-w-[80%] rounded-lg px-4 py-3", isUser ? "bg-blue-600 text-white" : "bg-white border border-gray-200 text-gray-800")}>
        {isUser ? (
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="prose prose-sm max-w-none prose-pre:bg-gray-900 prose-pre:text-gray-100">
            <ReactMarkdown rehypePlugins={[rehypeHighlight]}>{message.content}</ReactMarkdown>
          </div>
        )}
        {!isUser && message.relatedTopics && message.relatedTopics.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {message.relatedTopics.map((topic) => (
              <span key={topic} className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded-full">{topic}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
