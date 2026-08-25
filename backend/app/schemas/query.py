from pydantic import BaseModel, Field


class ChatTurn(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    history: list[ChatTurn] | None = None


class SourceRef(BaseModel):
    source_type: str  # "kb" | "web"
    title: str
    similarity: float | None = None
    url: str | None = None
    source_file: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceRef]
    used_web_fallback: bool
