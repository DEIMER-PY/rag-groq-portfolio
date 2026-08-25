from app.config import settings
from app.core.prompts import OUT_OF_SCOPE_MESSAGE
from app.services.groq_client import check_scope_with_llm

IN_SCOPE_KEYWORDS = (
    "código", "codigo", "programa", "programaci", "software", "desarroll",
    "frontend", "backend", "full-stack", "fullstack", "html", "css", "javascript",
    "typescript", "react", "vue", "angular", "node", "express", "python", "fastapi",
    "django", "java", "sql", "postgres", "mysql", "mongodb", "redis", "orm",
    "api", "rest", "graphql", "jwt", "oauth", "cors", "docker", "kubernetes",
    "ci/cd", "github actions", "devops", "test", "pytest", "jest", "vitest",
    "embedding", "vector", "rag", "llm", "groq", "langchain", "llamaindex",
    "mcp", "agente", "clean code", "solid", "hexagonal", "scrum", "kanban",
    "git", "base de datos", "algoritmo", "framework", "librería", "libreria",
)


class InputTooLongError(Exception):
    pass


def validate_input_length(query: str) -> None:
    if len(query) > settings.max_input_chars:
        raise InputTooLongError(
            f"La pregunta supera el límite de {settings.max_input_chars} caracteres."
        )


def is_in_scope(query: str) -> bool:
    lowered = query.lower()
    if any(keyword in lowered for keyword in IN_SCOPE_KEYWORDS):
        return True
    return check_scope_with_llm(query)


def out_of_scope_response() -> str:
    return OUT_OF_SCOPE_MESSAGE
