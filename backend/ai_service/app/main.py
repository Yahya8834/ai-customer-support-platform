from fastapi import FastAPI
from pydantic import BaseModel
from app.config import settings
from app.providers.ollama import OllamaEmbeddingProvider
from pydantic import BaseModel, field_validator
from fastapi import FastAPI, HTTPException



app = FastAPI()

class EmbeddingRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text cannot be empty")

        return value


embedding_provider = OllamaEmbeddingProvider(
    base_url=settings.bge_api_url,
    model=settings.bge_model,
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/v1/embeddings")
def create_embedding(request: EmbeddingRequest):
    try:
        embedding = embedding_provider.generate(request.text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Embedding generation failed",
        ) from exc

    return {"embedding": embedding}