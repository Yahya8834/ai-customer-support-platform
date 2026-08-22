class ChatService:
    def __init__(self, chat_graph):
        self.chat_graph = chat_graph

    def generate(
        self,
        *,
        workspace_uuid: str,
        prompt: str,
    ) -> str:
        return self.chat_graph.run(
            workspace_uuid=workspace_uuid,
            prompt=prompt,
        )