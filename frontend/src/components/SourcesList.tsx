import type { SourceRef } from "../types/chat";
import { SourceBadge } from "./SourceBadge";

export function SourcesList({ sources }: { sources: SourceRef[] }) {
  if (sources.length === 0) return null;

  return (
    <div className="sources-list" role="list" aria-label="Fuentes">
      {sources.map((source, i) => (
        <SourceBadge key={`${source.source_type}-${i}`} source={source} />
      ))}
    </div>
  );
}
