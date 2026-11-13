from crewai import Agent

from agente.tasks import (
    create_concept_task,
    create_diagnostic_task,
    create_example_task,
    create_review_task,
)


def fake_agent() -> Agent:
    return Agent(
        role="Agente de teste",
        goal="Testar Tasks",
        backstory="Agente usado apenas nos testes.",
        llm="fake-llm",
        verbose=False,
    )


def test_specialist_tasks_include_question_and_context() -> None:
    agent = fake_agent()

    tasks = (
        create_concept_task("O que é Iterator?", agent, "histórico"),
        create_example_task("Mostre um exemplo", agent, "histórico"),
        create_diagnostic_task("Onde errei?", agent, "histórico"),
    )

    assert all("histórico" in task.description for task in tasks)
    assert all(task.agent is agent for task in tasks)


def test_review_task_receives_previous_tasks() -> None:
    agent = fake_agent()
    specialist_task = create_concept_task("O que é Iterator?", agent)

    review = create_review_task(
        "O que é Iterator?",
        agent,
        [specialist_task],
        "contexto anterior",
    )

    assert review.context == [specialist_task]
    assert "contexto anterior" in review.description
