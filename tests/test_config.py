import pytest

from agente.config import Settings, get_settings


def test_settings_validates_values() -> None:
    config = Settings(
        ollama_base_url="http://ollama:11434",
        ollama_model="qwen2.5:3b",
        temperature=0.4,
    )

    assert str(config.ollama_base_url) == "http://ollama:11434/"
    assert config.ollama_model_id == "ollama/qwen2.5:3b"


@pytest.mark.parametrize(
    "field,value",
    [
        ("ollama_base_url", "not-a-url"),
        ("ollama_model", ""),
        ("temperature", -0.1),
    ],
)
def test_settings_rejects_invalid_values(field: str, value: object) -> None:
    with pytest.raises(ValueError):
        Settings(**{field: value})


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("OLLAMA_MODEL", "cached-model")

    first = get_settings()
    second = get_settings()

    assert first is second
    assert first.ollama_model == "cached-model"
    get_settings.cache_clear()
