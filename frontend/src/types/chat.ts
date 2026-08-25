export type SourceType = "kb" | "web";

export interface SourceRef {
  source_type: SourceType;
  title: string;
  similarity?: number | null;
  url?: string | null;
  source_file?: string | null;
}

export interface QueryResponse {
  answer: string;
  sources: SourceRef[];
  used_web_fallback: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: SourceRef[];
}
