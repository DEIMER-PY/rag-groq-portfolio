import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { ChatMessage } from "../types/chat";
import { SourcesList } from "./SourcesList";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className="message-bubble" data-role={message.role}>
      <div className="message-content">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
      </div>
      {!isUser && message.sources && <SourcesList sources={message.sources} />}
    </div>
  );
}
