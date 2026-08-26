import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Notebook } from "./Notebook";
import * as notebookClient from "../api/notebookClient";

afterEach(() => {
  vi.restoreAllMocks();
  localStorage.clear();
});

describe("Notebook", () => {
  it("uploads a document and refreshes the sources list", async () => {
    vi.spyOn(notebookClient, "fetchNotebookSources")
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([{ source_title: "Mis notas", chunk_count: 3 }]);
    const uploadSpy = vi
      .spyOn(notebookClient, "uploadNotebookDocument")
      .mockResolvedValue({ title: "Mis notas", chunks_added: 3 });

    const user = userEvent.setup();
    render(<Notebook />);

    await user.type(screen.getByPlaceholderText(/título de la fuente/i), "Mis notas");
    await user.type(screen.getByPlaceholderText(/pega aquí el contenido/i), "contenido de prueba");
    await user.click(screen.getByRole("button", { name: /agregar fuente/i }));

    await waitFor(() => expect(uploadSpy).toHaveBeenCalled());
    await waitFor(() => expect(screen.getByText(/mis notas/i)).toBeInTheDocument());
  });

  it("disables the ask button while there is no question typed", async () => {
    vi.spyOn(notebookClient, "fetchNotebookSources").mockResolvedValue([]);
    render(<Notebook />);

    await waitFor(() => expect(screen.getByRole("button", { name: /enviar/i })).toBeDisabled());
  });

  it("sends a question and renders the answer with cited sources", async () => {
    vi.spyOn(notebookClient, "fetchNotebookSources").mockResolvedValue([
      { source_title: "doc.txt", chunk_count: 2 },
    ]);
    vi.spyOn(notebookClient, "queryNotebook").mockResolvedValue({
      answer: "El documento dice X",
      sources: ["doc.txt"],
    });

    const user = userEvent.setup();
    render(<Notebook />);

    await waitFor(() => expect(screen.getByText(/doc\.txt/)).toBeInTheDocument());

    await user.type(screen.getByPlaceholderText(/pregunta sobre tu documento/i), "¿qué dice?");
    await user.click(screen.getByRole("button", { name: /enviar/i }));

    await waitFor(() => expect(screen.getByText(/el documento dice x/i)).toBeInTheDocument());
  });
});
