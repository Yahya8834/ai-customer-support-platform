from .deepseek import DeepSeekClient


class OllamaDeepSeekClient(DeepSeekClient):
    def __init__(self, ollama):
        self.ollama = ollama

    def chat(self, prompt: str) -> str:
        response = self.ollama.chat(prompt)

        return response["message"]["content"]

    def stream(self, prompt: str):
        for chunk in self.ollama.stream(prompt):
            yield chunk["message"]["content"]