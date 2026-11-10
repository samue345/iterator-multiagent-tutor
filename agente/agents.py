from crewai import Agent

from .config import Settings
from .llm import create_llm
from .prompts import (
    CONCEPT_TUTOR_PROMPT,
    DIAGNOSTIC_TUTOR_PROMPT,
    EXAMPLE_TUTOR_PROMPT,
    REVIEWER_TUTOR_PROMPT,
)


def _create_agent(
    config: Settings,
    *,
    role: str,
    goal: str,
    backstory: str,
) -> Agent:
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=create_llm(config),
        verbose=False,
        allow_delegation=False,
    )


def create_concept_tutor(config: Settings) -> Agent:
    return _create_agent(
        config,
        role="Tutor conceitual",
        goal="Ensinar o padrão Iterator com precisão e clareza",
        backstory=CONCEPT_TUTOR_PROMPT,
    )


def create_example_tutor(config: Settings) -> Agent:
    return _create_agent(
        config,
        role="Exemplificador",
        goal="Produzir exemplos corretos e progressivos do padrão Iterator",
        backstory=EXAMPLE_TUTOR_PROMPT,
    )


def create_diagnostic_tutor(config: Settings) -> Agent:
    return _create_agent(
        config,
        role="Diagnosticador",
        goal="Identificar lacunas de compreensão e orientar o estudante",
        backstory=DIAGNOSTIC_TUTOR_PROMPT,
    )


def create_reviewer_tutor(config: Settings) -> Agent:
    return _create_agent(
        config,
        role="Revisor",
        goal="Revisar e consolidar respostas corretas e pedagógicas",
        backstory=REVIEWER_TUTOR_PROMPT,
    )
