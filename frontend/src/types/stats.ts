export interface ModuleCount {
  module: string;
  chunk_count: number;
}

export interface RecentQuery {
  query: string;
  in_scope: boolean;
  used_web_fallback: boolean;
  created_at: string;
}

export interface Stats {
  total_documents: number;
  documents_by_module: ModuleCount[];
  total_queries: number;
  in_scope_queries: number;
  web_fallback_queries: number;
  recent_queries: RecentQuery[];
}
