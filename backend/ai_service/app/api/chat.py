from fastapi import APIRouter
from pydantic import BaseModel, field_validator
from app.config import settings
from app.providers.llm.ollama import OllamaLLMProvider



router = APIRouter()

llm_provider = OllamaLLMProvider(
    base_url=settings.bge_api_url,
    model=settings.llm_model,
)


class ChatRequest(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("prompt cannot be empty")

        return value


@router.post("/v1/chat")
def generate_chat(request: ChatRequest):
    response = llm_provider.generate(request.prompt)

    return {"response": response}