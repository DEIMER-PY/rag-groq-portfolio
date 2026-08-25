import { useChat } from "../hooks/useChat";
import { ChatInput } from "./ChatInput";
import { MessageBubble } from "./MessageBubble";
import { TopicGuard } from "./TopicGuard";

export function ChatWindow() {
  const { messages, isLoading, error, send } = useChat();

  return (
    <div className="chat-window">
      <TopicGuard />
      <div className="messages" role="log">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && <div className="message-bubble" data-role="assistant">Pensando…</div>}
        {error && <div className="chat-error" role="alert">{error}</div>}
      </div>
      <ChatInput onSend={send} disabled={isLoading} />
    </div>
  );
}
