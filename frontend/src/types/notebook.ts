export interface NotebookSource {
  source_title: string;
  chunk_count: number;
}

export interface NotebookUploadResponse {
  title: string;
  chunks_added: number;
}

export interface NotebookQueryResponse {
  answer: string;
  sources: string[];
}

export interface NotebookMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}
