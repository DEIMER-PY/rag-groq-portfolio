from pydantic import BaseModel, Field


class NotebookUploadRequest(BaseModel):
    notebook_id: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=20_000)


class NotebookUploadResponse(BaseModel):
    title: str
    chunks_added: int


class NotebookSource(BaseModel):
    source_title: str
    chunk_count: int


class NotebookQueryRequest(BaseModel):
    notebook_id: str = Field(..., min_length=1, max_length=100)
    query: str = Field(..., min_length=1, max_length=2000)


class NotebookQueryResponse(BaseModel):
    answer: str
    sources: list[str]
