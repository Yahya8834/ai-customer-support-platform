from typing import TypedDict
from langgraph.graph import END, START, StateGraph



class ChatState(TypedDict):
    workspace_uuid: str
    prompt: str
    response: str


class ChatGraph:
    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

        builder = StateGraph(ChatState)

        builder.add_node("generate", self._generate)
        builder.add_edge(START, "generate")
        builder.add_edge("generate", END)

        self.graph = builder.compile()

    def _generate(self, state: ChatState) -> dict:
        response = self.llm_provider.generate(state["prompt"])

        return {"response": response}

    def run(
        self,
        *,
        workspace_uuid: str,
        prompt: str,
    ) -> str:
        result = self.graph.invoke({
            "workspace_uuid": workspace_uuid,
            "prompt": prompt,
            "response": "",
        })

        return result["response"]