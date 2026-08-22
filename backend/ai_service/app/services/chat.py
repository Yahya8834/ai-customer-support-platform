class ChatService:
    def __init__(self, chat_graph):
        self.chat_graph = chat_graph

    def generate(self, prompt: str) -> str:
        return self.chat_graph.run(prompt)