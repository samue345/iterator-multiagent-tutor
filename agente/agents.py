from crewai import Agent, LLM

from .config import Settings
from .prompts import CONCEPT_TUTOR_PROMPT


def create_concept_tutor(config: Settings) -> Agent:
    llm = LLM(
        model=f"ollama/{config.ollama_model}",
        base_url=config.ollama_base_url,
        temperature=config.temperature,
    )
    return Agent(
        role="Tutor conceitual",
        goal="Ensinar o padrão Iterator com precisão e clareza",
        backstory=CONCEPT_TUTOR_PROMPT,
        llm=llm,
        verbose=False,
    )
