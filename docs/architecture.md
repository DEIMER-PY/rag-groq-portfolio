# Arquitectura

```
┌─────────────────────┐        POST /query        ┌──────────────────────┐
│  Frontend            │ ─────────────────────────▶ │  Backend              │
│  React + Vite (SPA)  │                            │  FastAPI              │
│  Render Static Site  │ ◀───────────────────────── │  Render Web Service   │
└─────────────────────┘        JSON response        └──────────┬───────────┘
                                                                 │
                     ┌───────────────────────────────────────────┼───────────────────────────────┐
                     ▼                                            ▼                                 ▼
        ┌───────────────────────┐                 ┌─────────────────────────┐        ┌───────────────────────┐
        │ Embeddings locales     │                 │ Groq API                 │        │ DuckDuckGo Search       │
        │ sentence-transformers  │                 │ openai/gpt-oss-120b      │        │ (fallback, solo si la   │
        │ (MiniLM, 384 dims)     │                 │ openai/gpt-oss-20b       │        │ KB tiene baja confianza │
        └──────────┬─────────────┘                 │ (scope check + answer)  │        │ o se pide info reciente)│
                   ▼                                └─────────────────────────┘        └───────────────────────┘
        ┌───────────────────────┐
        │ Supabase (Postgres)    │
        │ extensión pgvector     │
        │ tabla documents +      │
        │ RPC match_documents    │
        └───────────────────────┘
```

## Flujo de una consulta

1. El usuario escribe una pregunta en el chat (React).
2. El frontend hace `POST /query` al backend (FastAPI), sin hablar nunca directo con Supabase.
3. El backend valida longitud de input y decide si la pregunta está **dentro de alcance**
   (heurística de keywords + fallback a un check rápido con `openai/gpt-oss-20b`). Si no lo
   está, responde una plantilla fija sin gastar retrieval ni el modelo grande.
4. Si está en alcance: se genera el embedding de la pregunta (mismo modelo usado en la
   ingesta) y se llama a la función `match_documents` de Supabase (similarity search sobre
   pgvector, índice HNSW).
5. Si la similitud máxima es baja, o la pregunta tiene señales de "actualidad" (ej. "2026",
   "reciente"), se dispara un fallback de búsqueda web con DuckDuckGo.
6. Se arma el prompt final con el `SYSTEM_PROMPT` de guardrails + el contexto recuperado
   (etiquetado `<contexto_kb>`/`<contexto_web>`, explícitamente marcado como datos, no
   instrucciones) + la pregunta.
7. Se llama a Groq (`openai/gpt-oss-120b`) para generar la respuesta.
8. El backend devuelve `{ answer, sources, used_web_fallback }`; el frontend renderiza la
   respuesta en markdown y las fuentes como chips distinguibles (KB vs web).

## Por qué estas decisiones

- **Sin LangChain/LlamaIndex**: el pipeline es un flujo lineal de 5-6 pasos bien definidos;
  código propio es más transparente para un proyecto de portafolio y evita una dependencia
  pesada para un problema que no la necesita.
- **Embeddings locales (MiniLM)**: cero costo por token, sin llamadas de red adicionales en
  la ingesta ni en cada consulta.
- **pgvector sobre Supabase**: base de datos relacional real (no solo un vector store
  embebido), free tier, y acceso directo vía SQL para debugging.
- **Guardrails explícitos en el prompt**: el contexto recuperado (de la KB o de la web) se
  trata siempre como datos citados, nunca como instrucciones — mitigación básica pero real
  contra prompt injection vía contenido recuperado.
