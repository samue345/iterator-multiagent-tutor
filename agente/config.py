import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    temperature: float = float(os.getenv("MODEL_TEMPERATURE", "0.2"))

    @property
    def ollama_model_id(self) -> str:
        return f"ollama/{self.ollama_model}"


settings = Settings()
