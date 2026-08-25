import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ChatInput } from "./ChatInput";

describe("ChatInput", () => {
  it("disables the send button when the input is empty", () => {
    render(<ChatInput onSend={() => {}} maxChars={500} />);

    expect(screen.getByRole("button", { name: /enviar/i })).toBeDisabled();
  });

  it("disables the send button when the character limit is exceeded", async () => {
    const user = userEvent.setup();
    render(<ChatInput onSend={() => {}} maxChars={10} />);

    await user.type(screen.getByRole("textbox"), "esto tiene mas de diez caracteres");

    expect(screen.getByRole("button", { name: /enviar/i })).toBeDisabled();
    expect(screen.getByText(/\/10/)).toHaveAttribute("data-over-limit", "true");
  });

  it("calls onSend with the trimmed text and clears the input", async () => {
    const user = userEvent.setup();
    const onSend = vi.fn();
    render(<ChatInput onSend={onSend} maxChars={500} />);

    const textarea = screen.getByRole("textbox");
    await user.type(textarea, "  ¿qué es SOLID?  ");
    await user.click(screen.getByRole("button", { name: /enviar/i }));

    expect(onSend).toHaveBeenCalledWith("¿qué es SOLID?");
    expect(textarea).toHaveValue("");
  });

  it("does not call onSend while disabled", async () => {
    const user = userEvent.setup();
    const onSend = vi.fn();
    render(<ChatInput onSend={onSend} disabled maxChars={500} />);

    await user.type(screen.getByRole("textbox"), "hola");
    expect(screen.getByRole("button", { name: /enviar/i })).toBeDisabled();
  });
});
