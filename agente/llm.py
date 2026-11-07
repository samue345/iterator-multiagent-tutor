from crewai import LLM

from .config import Settings


def create_llm(config: Settings) -> LLM:
    """Cria o adaptador unico do sistema para o modelo local Ollama."""
    return LLM(
        model=f"ollama/{config.ollama_model}",
        base_url=config.ollama_base_url,
        temperature=config.temperature,
    )
