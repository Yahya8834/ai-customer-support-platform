from unittest.mock import Mock
from app.services.chat_graph import ChatGraph



def test_chat_graph_generates_response():
    llm_provider = Mock()
    llm_provider.generate.return_value = "Hello"

    graph = ChatGraph(llm_provider)

    response = graph.run("hello")

    assert response == "Hello"