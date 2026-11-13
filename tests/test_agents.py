import pytest

from agente import agents
from agente.config import Settings


@pytest.mark.parametrize(
    ("factory_name", "role"),
    [
        ("create_concept_tutor", "Tutor conceitual"),
        ("create_example_tutor", "Exemplificador"),
        ("create_diagnostic_tutor", "Diagnosticador"),
        ("create_reviewer_tutor", "Revisor"),
    ],
)
def test_agent_factories_create_specialists(
    monkeypatch: pytest.MonkeyPatch,
    factory_name: str,
    role: str,
) -> None:
    class FakeAgent:
        def __init__(self, **kwargs: object) -> None:
            self.__dict__.update(kwargs)

    monkeypatch.setattr(agents, "create_llm", lambda config: "fake-llm")
    monkeypatch.setattr(agents, "Agent", FakeAgent)
    factory = getattr(agents, factory_name)

    agent = factory(Settings())

    assert agent.role == role
    assert agent.allow_delegation is False
    assert agent.llm == "fake-llm"
