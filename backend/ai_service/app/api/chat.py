from fastapi import APIRouter
from pydantic import BaseModel, field_validator
from uuid import UUID
from app.config import settings
from app.providers.llm.ollama import OllamaLLMProvider
from app.services.chat import ChatService
from app.services.chat_graph import ChatGraph
from app.providers.llm.factory import LLMProviderFactory
from app.providers.llm.qwen import QwenLLMProvider



router = APIRouter()

llm_provider_factory = LLMProviderFactory(
    providers={
        "ollama": OllamaLLMProvider(
            base_url=settings.llm_api_url,
        ),

        "qwen": QwenLLMProvider(
            api_key=settings.qwen_inference_key,
        ),
    }
)

chat_graph = ChatGraph(llm_provider_factory)

chat_service = ChatService(chat_graph)


class ChatRequest(BaseModel):
    workspace_uuid: UUID
    provider: str
    model: str
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("prompt cannot be empty")

        return value
    

@router.post("/v1/chat")
def generate_chat(request: ChatRequest):
    response = chat_service.generate(
        workspace_uuid=str(request.workspace_uuid),
        provider=request.provider,
        model=request.model,
        prompt=request.prompt,
    )
    return {"response": response}