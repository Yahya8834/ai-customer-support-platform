from collections.abc import Iterator


class ChatService:
    def __init__(self, chat_graph):
        self.chat_graph = chat_graph

    def generate(
        self,
        *,
        workspace_uuid: str,
        provider: str,
        model: str,
        prompt: str,
    ) -> str:
        return self.chat_graph.run(
            workspace_uuid=workspace_uuid,
            provider=provider,
            model=model,
            prompt=prompt,
        )

    def stream(
        self,
        *,
        workspace_uuid: str,
        provider: str,
        model: str,
        prompt: str,
    ) -> Iterator[str]:
        return self.chat_graph.stream(
            workspace_uuid=workspace_uuid,
            provider=provider,
            model=model,
            prompt=prompt,
        )