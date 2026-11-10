from functools import lru_cache
from typing import Annotated

from pydantic import AnyHttpUrl, Field, StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        frozen=True,
        validate_default=True,
    )

    ollama_base_url: AnyHttpUrl = "http://localhost:11434"
    ollama_model: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1),
    ] = "qwen2.5:3b"
    temperature: float = Field(default=0.2, ge=0)

    @property
    def ollama_model_id(self) -> str:
        return f"ollama/{self.ollama_model}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
