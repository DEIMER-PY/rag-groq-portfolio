import { API_URL } from "../config";
import type { NotebookQueryResponse, NotebookSource, NotebookUploadResponse } from "../types/notebook";

async function handle<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Error ${response.status}`);
  }
  return response.json();
}

export async function uploadNotebookDocument(
  notebookId: string,
  title: string,
  content: string
): Promise<NotebookUploadResponse> {
  const response = await fetch(`${API_URL}/notebooks/upload`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notebook_id: notebookId, title, content }),
  });
  return handle(response);
}

export async function fetchNotebookSources(notebookId: string): Promise<NotebookSource[]> {
  const response = await fetch(`${API_URL}/notebooks/${notebookId}/sources`);
  return handle(response);
}

export async function queryNotebook(notebookId: string, query: string): Promise<NotebookQueryResponse> {
  const response = await fetch(`${API_URL}/notebooks/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notebook_id: notebookId, query }),
  });
  return handle(response);
}
