import { useState } from "react";
import { MAX_INPUT_CHARS } from "../config";

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
  maxChars?: number;
}

export function ChatInput({ onSend, disabled, maxChars = MAX_INPUT_CHARS }: ChatInputProps) {
  const [value, setValue] = useState("");

  const trimmed = value.trim();
  const overLimit = value.length > maxChars;
  const canSend = trimmed.length > 0 && !overLimit && !disabled;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSend) return;
    onSend(trimmed);
    setValue("");
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Pregunta algo sobre desarrollo de software..."
        rows={2}
        disabled={disabled}
      />
      <div className="chat-input-footer">
        <span data-over-limit={overLimit}>
          {value.length}/{maxChars}
        </span>
        <button type="submit" disabled={!canSend}>
          Enviar
        </button>
      </div>
    </form>
  );
}
