import type { SourceRef } from "../types/chat";

export function SourceBadge({ source }: { source: SourceRef }) {
  const isKb = source.source_type === "kb";

  return (
    <a
      className="source-badge"
      data-type={source.source_type}
      href={source.url ?? undefined}
      target={source.url ? "_blank" : undefined}
      rel={source.url ? "noreferrer" : undefined}
      title={source.source_file ?? source.url ?? source.title}
    >
      <span aria-hidden="true">{isKb ? "📚" : "🌐"}</span>
      {source.title}
    </a>
  );
}
