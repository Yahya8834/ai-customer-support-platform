from unittest.mock import Mock
from app.services.chat import ChatService



def test_chat_service_generates_response():
    chat_graph = Mock()
    chat_graph.run.return_value = "Hello"

    service = ChatService(chat_graph)

    response = service.generate("hello")

    assert response == "Hello"
    chat_graph.run.assert_called_once_with("hello")