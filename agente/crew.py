from crewai import Crew, Process, Task

from .agents import (
    create_concept_tutor,
    create_diagnostic_tutor,
    create_example_tutor,
    create_reviewer_tutor,
)
from .config import Settings
from .router import Flow
from .tasks import (
    create_concept_task,
    create_diagnostic_task,
    create_example_task,
    create_review_task,
)


def create_crew(
    config: Settings,
    question: str,
    flow: Flow,
    context: str = "",
) -> Crew:
    if flow is Flow.EXAMPLE:
        specialist = create_example_tutor(config)
        specialist_task = create_example_task(question, specialist, context)
    elif flow is Flow.DIAGNOSTIC:
        specialist = create_diagnostic_tutor(config)
        specialist_task = create_diagnostic_task(question, specialist, context)
    else:
        specialist = create_concept_tutor(config)
        specialist_task = create_concept_task(question, specialist, context)

    reviewer = create_reviewer_tutor(config)
    review_task = create_review_task(
        question,
        reviewer,
        [specialist_task],
        conversation_context=context,
    )

    return Crew(
        agents=[specialist, reviewer],
        tasks=[specialist_task, review_task],
        process=Process.sequential,
        verbose=False,
    )


def run_crew(
    config: Settings,
    question: str,
    flow: Flow,
    context: str = "",
) -> object:
    result = create_crew(config, question, flow, context).kickoff()
    return getattr(result, "raw", result)
