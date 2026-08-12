from abc import ABC, abstractmethod
from collections.abc import Iterator


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a complete response."""
        raise NotImplementedError

    @abstractmethod
    def stream(self, prompt: str) -> Iterator[str]:
        """Stream a response as chunks."""
        raise NotImplementedError