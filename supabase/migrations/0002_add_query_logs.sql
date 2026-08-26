-- Tabla de logging de consultas, usada por el dashboard (GET /stats).
-- No guarda la respuesta generada, solo metadata suficiente para métricas.

create table if not exists query_logs (
  id bigserial primary key,
  query text not null,
  in_scope boolean not null,
  max_similarity float,
  used_web_fallback boolean not null default false,
  created_at timestamptz default now()
);

create index if not exists query_logs_created_at_idx on query_logs (created_at desc);

alter table query_logs enable row level security;

-- RPCs de agregación para el dashboard (GET /stats). PostgREST no soporta GROUP BY
-- directamente desde el query builder, así que se exponen como funciones SQL.

create or replace function documents_by_module()
returns table (module text, chunk_count bigint)
language sql stable as $$
  select module, count(*) as chunk_count
  from documents
  group by module
  order by module;
$$;

create or replace function query_log_summary()
returns table (total_queries bigint, in_scope_queries bigint, web_fallback_queries bigint)
language sql stable as $$
  select
    count(*) as total_queries,
    count(*) filter (where in_scope) as in_scope_queries,
    count(*) filter (where used_web_fallback) as web_fallback_queries
  from query_logs;
$$;
