from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    @abstractmethod
    def generate(self, text: str) -> list[float]:
        pass