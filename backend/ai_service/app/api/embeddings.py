from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.config import settings
from app.providers.embedding.ollama import OllamaEmbeddingProvider


router = APIRouter()

embedding_provider = OllamaEmbeddingProvider(
    base_url=settings.bge_api_url,
    model=settings.bge_model,
)


class EmbeddingRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text cannot be empty")

        return value


@router.post("/v1/embeddings")
def create_embedding(request: EmbeddingRequest):
    try:
        embedding = embedding_provider.embed(request.text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Embedding generation failed",
        ) from exc

    return {"embedding": embedding}