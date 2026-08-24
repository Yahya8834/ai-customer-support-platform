from unittest.mock import Mock
from app.services.chat_graph import ChatGraph


def test_chat_graph_generates_response():
    llm_provider = Mock()
    llm_provider.generate.return_value = "Hello"

    graph = ChatGraph(llm_provider)

    response = graph.run(
        workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
        prompt="hello",
    )

    assert response == "Hello"

    llm_provider.generate.assert_called_once_with("hello")