-- Extensión pgvector y esquema base para el RAG.
-- Aplicada al proyecto Supabase "rag-groq-portfolio" vía MCP (apply_migration).

create extension if not exists vector;

create table if not exists documents (
  id bigserial primary key,
  content text not null,
  embedding vector(384),          -- 384 dims = sentence-transformers/all-MiniLM-L6-v2
  source_file text not null,      -- ruta relativa dentro de corpus/, ej. 'ia-rag/rag-arquitectura.md'
  module text not null,           -- carpeta de primer nivel dentro de corpus/
  section_title text,             -- último heading ##/### antes del chunk
  chunk_index int not null,       -- posición secuencial del chunk dentro del documento fuente
  token_count int,
  created_at timestamptz default now()
);

-- HNSW: no requiere entrenamiento previo (a diferencia de IVF) y da buen recall/latencia
-- para un corpus de tamaño pequeño-mediano como este.
create index if not exists documents_embedding_idx
  on documents using hnsw (embedding vector_cosine_ops);

create index if not exists documents_module_idx on documents (module);

-- RPC de similarity search usada por backend/app/services/retrieval.py.
-- Retorna 1 - distancia_coseno como "similarity" (0 a 1, mayor es más similar).
create or replace function match_documents (
  query_embedding vector(384),
  match_count int default 5,
  filter_module text default null,
  min_similarity float default 0.35
)
returns table (
  id bigint,
  content text,
  source_file text,
  module text,
  section_title text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    d.id,
    d.content,
    d.source_file,
    d.module,
    d.section_title,
    1 - (d.embedding <=> query_embedding) as similarity
  from documents d
  where (filter_module is null or d.module = filter_module)
    and 1 - (d.embedding <=> query_embedding) > min_similarity
  order by d.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Solo el backend (con SUPABASE_SERVICE_ROLE_KEY, que bypassa RLS) accede a esta tabla.
-- El frontend nunca recibe una key con acceso a "documents".
alter table documents enable row level security;
