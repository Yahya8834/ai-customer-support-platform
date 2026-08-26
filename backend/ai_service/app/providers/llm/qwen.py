from openai import OpenAI
from app.providers.llm.base import LLMProvider



class QwenLLMProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://inference.do-ai.run/v1/",
            api_key=api_key,
        )


    def generate(self, prompt: str, model: str) -> str:
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("response content is missing")

        return content