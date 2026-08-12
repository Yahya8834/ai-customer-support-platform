from abc import ABC, abstractmethod
from collections.abc import Iterator


class DeepSeekClient(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Generate a complete response."""
        raise NotImplementedError

    @abstractmethod
    def stream(self, prompt: str) -> Iterator[str]:
        """Stream response chunks."""
        raise NotImplementedError