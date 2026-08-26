import { useCallback, useEffect, useState } from "react";
import { fetchNotebookSources, queryNotebook, uploadNotebookDocument } from "../api/notebookClient";
import type { NotebookMessage, NotebookSource } from "../types/notebook";

const STORAGE_KEY = "rag-ai-notebook-id";

function getOrCreateNotebookId(): string {
  const existing = localStorage.getItem(STORAGE_KEY);
  if (existing) return existing;
  const id = crypto.randomUUID();
  localStorage.setItem(STORAGE_KEY, id);
  return id;
}

export function useNotebook() {
  const [notebookId] = useState(getOrCreateNotebookId);
  const [sources, setSources] = useState<NotebookSource[]>([]);
  const [messages, setMessages] = useState<NotebookMessage[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshSources = useCallback(async () => {
    try {
      setSources(await fetchNotebookSources(notebookId));
    } catch {
      // silencioso: la lista de fuentes es informativa, no bloquea el chat
    }
  }, [notebookId]);

  useEffect(() => {
    refreshSources();
  }, [refreshSources]);

  const upload = useCallback(
    async (title: string, content: string) => {
      setIsUploading(true);
      setError(null);
      try {
        await uploadNotebookDocument(notebookId, title, content);
        await refreshSources();
      } catch (err) {
        setError(err instanceof Error ? err.message : "No se pudo subir el documento.");
      } finally {
        setIsUploading(false);
      }
    },
    [notebookId, refreshSources]
  );

  const send = useCallback(
    async (query: string) => {
      setMessages((prev) => [...prev, { id: crypto.randomUUID(), role: "user", content: query }]);
      setIsSending(true);
      setError(null);
      try {
        const response = await queryNotebook(notebookId, query);
        setMessages((prev) => [
          ...prev,
          { id: crypto.randomUUID(), role: "assistant", content: response.answer, sources: response.sources },
        ]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "No se pudo consultar el notebook.");
      } finally {
        setIsSending(false);
      }
    },
    [notebookId]
  );

  return { notebookId, sources, messages, isUploading, isSending, error, upload, send };
}
