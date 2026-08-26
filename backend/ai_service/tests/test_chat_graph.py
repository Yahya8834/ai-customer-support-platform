from unittest.mock import Mock
from app.services.chat_graph import ChatGraph



def test_chat_graph_generates_response():
    llm_provider = Mock()
    llm_provider.generate.return_value = "Hello"

    llm_provider_factory = Mock()
    llm_provider_factory.get.return_value = llm_provider

    graph = ChatGraph(llm_provider_factory)

    response = graph.run(
        workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
        model="deepseek-smart",
        prompt="hello",
    )

    assert response == "Hello"

    llm_provider_factory.get.assert_called_once_with(
        "deepseek-smart",
    )

    llm_provider.generate.assert_called_once_with(
        "hello",
    )