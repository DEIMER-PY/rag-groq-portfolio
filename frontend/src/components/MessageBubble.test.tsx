import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { ChatMessage } from "../types/chat";
import { MessageBubble } from "./MessageBubble";

describe("MessageBubble", () => {
  it("renders markdown content", () => {
    const message: ChatMessage = { id: "1", role: "assistant", content: "**hola** mundo" };
    render(<MessageBubble message={message} />);

    expect(screen.getByText("hola")).toBeInTheDocument();
  });

  it("shows a kb source badge for knowledge-base sources", () => {
    const message: ChatMessage = {
      id: "1",
      role: "assistant",
      content: "Respuesta",
      sources: [{ source_type: "kb", title: "RAG arquitectura", source_file: "ia-rag/rag-arquitectura.md" }],
    };
    render(<MessageBubble message={message} />);

    const badge = screen.getByText("RAG arquitectura");
    expect(badge.closest(".source-badge")).toHaveAttribute("data-type", "kb");
  });

  it("shows a web source badge for web sources", () => {
    const message: ChatMessage = {
      id: "1",
      role: "assistant",
      content: "Respuesta",
      sources: [{ source_type: "web", title: "Ejemplo", url: "https://example.com" }],
    };
    render(<MessageBubble message={message} />);

    const badge = screen.getByText("Ejemplo");
    expect(badge.closest(".source-badge")).toHaveAttribute("data-type", "web");
  });

  it("does not render a sources list for user messages", () => {
    const message: ChatMessage = { id: "1", role: "user", content: "hola" };
    render(<MessageBubble message={message} />);

    expect(screen.queryByRole("list", { name: /fuentes/i })).not.toBeInTheDocument();
  });
});
