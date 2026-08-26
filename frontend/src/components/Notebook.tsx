import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useNotebook } from "../hooks/useNotebook";

const MAX_NOTEBOOK_CHARS = 20_000;

export function Notebook() {
  const { sources, messages, isUploading, isSending, error, upload, send } = useNotebook();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [question, setQuestion] = useState("");

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;
    await upload(title.trim(), content.trim());
    setTitle("");
    setContent("");
  };

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isSending) return;
    const q = question.trim();
    setQuestion("");
    await send(q);
  };

  return (
    <div className="notebook">
      <p className="notebook-intro">
        Pega un documento propio (notas, un artículo, código) y pregúntale solo a ese
        contenido — como un NotebookLM en miniatura. No usa la base de conocimiento general
        ni tiene restricción de tema.
      </p>

      <form className="notebook-upload" onSubmit={handleUpload}>
        <input
          type="text"
          placeholder="Título de la fuente (ej. Notas de la reunión)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
        />
        <textarea
          placeholder="Pega aquí el contenido del documento…"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={5}
          maxLength={MAX_NOTEBOOK_CHARS}
        />
        <div className="notebook-upload-footer">
          <span>{content.length}/{MAX_NOTEBOOK_CHARS}</span>
          <button type="submit" disabled={isUploading || !title.trim() || !content.trim()}>
            {isUploading ? "Agregando…" : "Agregar fuente"}
          </button>
        </div>
      </form>

      {sources.length > 0 && (
        <div className="notebook-sources">
          <h3>Fuentes en este notebook</h3>
          <ul>
            {sources.map((s) => (
              <li key={s.source_title}>
                📄 {s.source_title} <span className="notebook-chunk-count">({s.chunk_count} fragmentos)</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="messages" role="log">
        {messages.map((m) => (
          <div className="message-bubble" data-role={m.role} key={m.id}>
            <div className="message-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
            </div>
            {m.sources && m.sources.length > 0 && (
              <div className="sources-list">
                {m.sources.map((s) => (
                  <span className="source-badge" data-type="kb" key={s}>
                    📄 {s}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        {isSending && <div className="message-bubble" data-role="assistant">Pensando…</div>}
        {error && <div className="chat-error" role="alert">{error}</div>}
      </div>

      <form className="chat-input" onSubmit={handleAsk}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={sources.length === 0 ? "Agrega una fuente primero…" : "Pregunta sobre tu documento…"}
          rows={2}
          disabled={isSending}
        />
        <div className="chat-input-footer">
          <span>{question.length}/500</span>
          <button type="submit" disabled={isSending || !question.trim()}>
            Enviar
          </button>
        </div>
      </form>
    </div>
  );
}
