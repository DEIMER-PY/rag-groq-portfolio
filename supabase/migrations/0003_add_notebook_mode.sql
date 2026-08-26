-- Modo "Notebook": el usuario pega/sube un documento propio y chatea solo sobre él,
-- en una sesión aislada por notebook_id (generado en el navegador, sin auth).
-- No comparte tabla con la KB curada (documents) para no contaminarla.

create table if not exists notebook_documents (
  id bigserial primary key,
  notebook_id text not null,
  content text not null,
  embedding vector(384),
  source_title text not null,
  chunk_index int not null,
  created_at timestamptz default now()
);

create index if not exists notebook_documents_notebook_id_idx on notebook_documents (notebook_id);
create index if not exists notebook_documents_embedding_idx
  on notebook_documents using hnsw (embedding vector_cosine_ops);

alter table notebook_documents enable row level security;

create or replace function match_notebook_documents(
  query_embedding vector(384),
  p_notebook_id text,
  match_count int default 6,
  min_similarity float default 0.0
)
returns table (
  content text,
  source_title text,
  chunk_index int,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    d.content,
    d.source_title,
    d.chunk_index,
    1 - (d.embedding <=> query_embedding) as similarity
  from notebook_documents d
  where d.notebook_id = p_notebook_id
    and 1 - (d.embedding <=> query_embedding) > min_similarity
  order by d.embedding <=> query_embedding
  limit match_count;
end;
$$;

create or replace function notebook_sources(p_notebook_id text)
returns table (source_title text, chunk_count bigint)
language sql stable as $$
  select source_title, count(*) as chunk_count
  from notebook_documents
  where notebook_id = p_notebook_id
  group by source_title
  order by min(chunk_index);
$$;
