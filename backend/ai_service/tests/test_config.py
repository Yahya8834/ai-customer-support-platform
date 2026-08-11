from app.config import settings


def test_bge_configuration_is_loaded():
    assert settings.bge_api_url == "http://host.docker.internal:11434"
    assert settings.bge_model == "bge-m3:567m"