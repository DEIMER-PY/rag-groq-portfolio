import { API_URL } from "../config";
import type { QueryResponse } from "../types/chat";

export class RagApiError extends Error {}

export async function sendQuery(query: string, signal?: AbortSignal): Promise<QueryResponse> {
  const response = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
    signal,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new RagApiError(body?.detail ?? `Error ${response.status} al consultar el asistente`);
  }

  return response.json();
}
