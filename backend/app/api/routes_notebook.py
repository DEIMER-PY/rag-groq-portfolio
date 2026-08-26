from fastapi import APIRouter, Request

from app.core.rate_limit import limiter
from app.schemas.notebook import (
    NotebookQueryRequest,
    NotebookQueryResponse,
    NotebookSource,
    NotebookUploadRequest,
    NotebookUploadResponse,
)
from app.services import notebook

router = APIRouter(prefix="/notebooks")


@router.post("/upload", response_model=NotebookUploadResponse)
@limiter.limit("20/minute")
async def upload(request: Request, body: NotebookUploadRequest) -> NotebookUploadResponse:
    return notebook.upload_document(body.notebook_id, body.title, body.content)


@router.get("/{notebook_id}/sources", response_model=list[NotebookSource])
async def sources(notebook_id: str) -> list[NotebookSource]:
    return notebook.list_sources(notebook_id)


@router.post("/query", response_model=NotebookQueryResponse)
@limiter.limit("10/minute")
async def query(request: Request, body: NotebookQueryRequest) -> NotebookQueryResponse:
    return notebook.query_notebook(body.notebook_id, body.query)
