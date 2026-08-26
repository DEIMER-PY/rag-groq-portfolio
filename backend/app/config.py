from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    groq_scope_check_model: str = "openai/gpt-oss-20b"
    groq_scope_check_max_tokens: int = 300

    supabase_url: str = ""
    supabase_service_role_key: str = ""

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    match_count: int = 5
    min_similarity: float = 0.35

    max_input_chars: int = 500
    max_output_tokens: int = 700

    cors_allow_origin: str = "http://localhost:5173"

    enable_web_search_fallback: bool = True


settings = Settings()
