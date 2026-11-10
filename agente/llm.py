from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from crewai import LLM

from .config import Settings


def create_llm(config: Settings) -> LLM:
    check_ollama_available(config)
    return LLM(
        model=config.ollama_model_id,
        base_url=str(config.ollama_base_url),
        temperature=config.temperature,
    )


def check_ollama_available(config: Settings, timeout: float = 2.0) -> None:
    health_url = f"{str(config.ollama_base_url).rstrip('/')}/api/tags"
    try:
        with urlopen(health_url, timeout=timeout) as response:
            if response.status >= 400:
                raise RuntimeError(
                    f"Ollama respondeu com status HTTP {response.status}."
                )
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(
            "Ollama está indisponível. Inicie o servidor e verifique "
            f"OLLAMA_BASE_URL ({str(config.ollama_base_url)})."
        ) from exc
