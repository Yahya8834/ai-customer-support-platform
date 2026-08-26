from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock



client = TestClient(app)


@patch(
    "app.api.embeddings.embedding_provider.embed",
    return_value=[0.1] * 1024,
)
def test_create_embedding(mock_generate):
    response = client.post(
        "/v1/embeddings",
        json={"text": "hello world"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "embedding" in data
    assert isinstance(data["embedding"], list)
    assert len(data["embedding"]) == 1024


def test_create_embedding_requires_text():
    response = client.post(
        "/v1/embeddings",
        json={},
    )

    assert response.status_code == 422


def test_create_embedding_rejects_empty_text():
    response = client.post(
        "/v1/embeddings",
        json={"text": ""},
    )

    assert response.status_code == 422


def test_create_embedding_rejects_whitespace_only_text():
    response = client.post(
        "/v1/embeddings",
        json={"text": "   "},
    )

    assert response.status_code == 422


@patch(
    "app.api.embeddings.embedding_provider.embed",
    side_effect=Exception("model unavailable"),
)
def test_create_embedding_handles_provider_failure(
    mock_generate,
):
    response = client.post(
        "/v1/embeddings",
        json={"text": "hello world"},
    )

    assert response.status_code == 500


@patch(
    "app.api.chat.llm_provider_factory.get",
    return_value="Hello from DeepSeek",
)
def test_generate_chat(mock_factory_get):
    mock_provider = MagicMock()
    mock_provider.generate.return_value = "Hello from service"
    mock_factory_get.return_value = mock_provider

    response = client.post(
        "/v1/chat",
        json={
            "workspace_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "model": "deepseek-smart",
            "prompt": "hello",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "response": "Hello from service",
    }


@patch(
    "app.api.chat.chat_service.generate",
    return_value="Hello from service",
)
def test_generate_chat_uses_chat_service(mock_generate):
    response = client.post(
        "/v1/chat",
        json={
            "workspace_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "model": "deepseek-smart",
            "prompt": "hello",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "response": "Hello from service",
    }

    mock_generate.assert_called_once_with(
        workspace_uuid="550e8400-e29b-41d4-a716-446655440000",
        model="deepseek-smart",
        prompt="hello",
    )


def test_generate_chat_requires_workspace_uuid():
    response = client.post(
        "/v1/chat",
        json={"prompt": "hello"},
    )

    assert response.status_code == 422