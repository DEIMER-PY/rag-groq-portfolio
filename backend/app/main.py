from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_health
from app.config import settings

app = FastAPI(title="RAG-AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_allow_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router)
