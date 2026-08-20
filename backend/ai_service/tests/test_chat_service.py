from unittest.mock import Mock
from app.services.chat import ChatService



def test_chat_service_generates_response():
    llm_provider = Mock()
    llm_provider.generate.return_value = "Hello"

    service = ChatService(llm_provider)

    response = service.generate("hello")

    assert response == "Hello"
    llm_provider.generate.assert_called_once_with("hello")