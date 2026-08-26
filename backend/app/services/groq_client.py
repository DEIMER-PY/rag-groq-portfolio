from functools import lru_cache

from openai import OpenAI

from app.config import settings
from app.core.prompts import SCOPE_CHECK_PROMPT, SYSTEM_PROMPT


@lru_cache
def get_groq_client() -> OpenAI | None:
    if not settings.groq_api_key:
        return None
    return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=settings.groq_api_key)


def check_scope_with_llm(query: str) -> bool:
    """Fallback used when the keyword heuristic in guardrails.py is inconclusive."""
    client = get_groq_client()
    if client is None:
        return True  # sin LLM disponible, no bloqueamos por este check

    response = client.chat.completions.create(
        model=settings.groq_scope_check_model,
        messages=[{"role": "user", "content": SCOPE_CHECK_PROMPT.format(query=query)}],
        temperature=0,
        # gpt-oss models are reasoning models: they spend tokens thinking before the
        # final SI/NO, so a tiny max_tokens truncates the answer before it appears.
        max_tokens=settings.groq_scope_check_max_tokens,
    )
    answer = (response.choices[0].message.content or "").strip().upper()
    return answer.startswith("SI")


def generate_answer(user_prompt: str) -> str:
    client = get_groq_client()
    if client is None:
        raise RuntimeError("Groq no está configurado (revisa GROQ_API_KEY)")

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=settings.max_output_tokens,
    )
    return response.choices[0].message.content or ""
