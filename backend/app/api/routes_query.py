from fastapi import APIRouter, HTTPException, Request

from app.core.rate_limit import limiter
from app.schemas.query import QueryRequest, QueryResponse
from app.services import rag_pipeline
from app.services.guardrails import InputTooLongError

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
@limiter.limit("10/minute")
async def query(request: Request, body: QueryRequest) -> QueryResponse:
    try:
        return rag_pipeline.answer_query(body.query)
    except InputTooLongError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
