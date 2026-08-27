from unittest.mock import Mock

from app.services.chat import ChatService


def test_chat_service_generates_response():
    chat_graph = Mock()
    chat_graph.run.return_value = "Hello"

    service = ChatService(chat_graph)

    response = service.generate(
        workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
        provider="ollama",
        model="deepseek-r1:8b",
        prompt="hello",
    )

    assert response == "Hello"

    chat_graph.run.assert_called_once_with(
        workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
        provider="ollama",
        model="deepseek-r1:8b",
        prompt="hello",
    )