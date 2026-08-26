import os


class Settings:
    def __init__(self):
        self.bge_api_url = os.environ["BGE_API_URL"]
        self.bge_model = os.environ["BGE_MODEL"]
        
        self.llm_api_url = os.environ["LLM_API_URL"]


settings = Settings()