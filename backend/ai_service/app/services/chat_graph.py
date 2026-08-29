from typing import TypedDict
from langgraph.graph import END, START, StateGraph



class ChatState(TypedDict):
    workspace_uuid: str
    provider: str
    model: str
    prompt: str
    response: str


class ChatGraph:
    def __init__(self, llm_provider_factory):
        self.llm_provider_factory = llm_provider_factory

        builder = StateGraph(ChatState)

        builder.add_node("generate", self._generate)
        builder.add_edge(START, "generate")
        builder.add_edge("generate", END)

        self.graph = builder.compile()

    def _generate(self, state: ChatState) -> dict:
        llm_provider = self.llm_provider_factory.get(
            state["provider"],
        )

        response = llm_provider.generate(
            state["prompt"],
            state["model"],
        )

        return {"response": response}

    def run(
        self,
        *,
        workspace_uuid: str,
        provider: str,
        model: str,
        prompt: str,
    ) -> str:
        result = self.graph.invoke({
            "workspace_uuid": workspace_uuid,
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "response": "",
        })

        return result["response"]
    
    def stream(
        self,
        *,
        workspace_uuid: str,
        provider: str,
        model: str,
        prompt: str,
    ):
        llm_provider = self.llm_provider_factory.get(
            provider,
        )

        return llm_provider.stream(
            prompt,
            model,
        )