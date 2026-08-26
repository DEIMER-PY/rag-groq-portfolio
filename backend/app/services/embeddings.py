from functools import lru_cache

from fastembed import TextEmbedding

from app.config import settings


@lru_cache
def get_embedding_model() -> TextEmbedding:
    # fastembed runs the model via ONNX Runtime instead of PyTorch. Same model,
    # same 384-dim output, but a fraction of the memory footprint — PyTorch +
    # sentence-transformers routinely pushed this process past Render's free-tier
    # 512MB RAM limit and got OOM-killed the moment the model first loaded.
    return TextEmbedding(model_name=settings.embedding_model_name)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return [vector.tolist() for vector in model.embed(texts)]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
