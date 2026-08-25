import re
from dataclasses import dataclass

DEFAULT_SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
HEADING_RE = re.compile(r"^(#{2,3})\s+(.*)$")


@dataclass
class Chunk:
    content: str
    section_title: str | None
    chunk_index: int


def _split_text(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    """Recursively splits text (no overlap) using the first separator that actually
    divides it, falling back to the next separator when a piece is still too large.
    Overlap is applied exactly once, by the caller, on the final flat list of pieces —
    applying it at every recursion level would compound and blow past chunk_size."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    separator = separators[0] if separators else ""
    remaining_separators = separators[1:]

    if separator:
        parts = [p for p in text.split(separator) if p.strip()]
    else:
        parts = list(text)

    if len(parts) == 1 and remaining_separators:
        return _split_text(text, chunk_size, remaining_separators)

    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current}{separator}{part}" if current else part
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)
        if len(part) > chunk_size and remaining_separators:
            chunks.extend(_split_text(part, chunk_size, remaining_separators))
            current = ""
        else:
            current = part

    if current:
        chunks.append(current)

    return chunks


def _apply_overlap(chunks: list[str], chunk_overlap: int) -> list[str]:
    if chunk_overlap <= 0 or len(chunks) < 2:
        return chunks

    overlapped = [chunks[0]]
    for chunk in chunks[1:]:
        previous = overlapped[-1]
        tail = previous[-chunk_overlap:] if len(previous) > chunk_overlap else previous
        overlapped.append(f"{tail}{chunk}")
    return overlapped


def chunk_markdown(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> list[Chunk]:
    """Splits a markdown document into chunks, tagging each with the last H2/H3
    heading seen before it so retrieval results can cite a meaningful section."""
    sections: list[tuple[str | None, str]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            if current_lines:
                sections.append((current_title, "\n".join(current_lines)))
            current_title = match.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines)))

    chunks: list[Chunk] = []
    index = 0
    for title, section_text in sections:
        pieces = _split_text(section_text, chunk_size, DEFAULT_SEPARATORS)
        pieces = _apply_overlap(pieces, chunk_overlap)
        for piece in pieces:
            if not piece.strip():
                continue
            chunks.append(Chunk(content=piece.strip(), section_title=title, chunk_index=index))
            index += 1

    return chunks
