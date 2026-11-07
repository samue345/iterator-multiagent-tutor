from crewai import Agent

from .config import Settings
from .llm import create_llm
from .prompts import CONCEPT_TUTOR_PROMPT


def create_concept_tutor(config: Settings) -> Agent:
    return Agent(
        role="Tutor conceitual",
        goal="Ensinar o padrão Iterator com precisão e clareza",
        backstory=CONCEPT_TUTOR_PROMPT,
        llm=create_llm(config),
        verbose=False,
    )
