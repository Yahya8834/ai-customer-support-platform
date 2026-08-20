class ChatService:
    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    def generate(self, prompt: str) -> str:
        return self.llm_provider.generate(prompt)