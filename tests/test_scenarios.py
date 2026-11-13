from agente.config import Settings
from agente.router import Flow, select_flow
from agente.system import TutorSystem


def test_conceptual_question_uses_concept_flow(monkeypatch) -> None:
    monkeypatch.setattr(
        "agente.router.create_llm",
        lambda config: type("Llm", (), {"call": lambda self, messages: "concept"})(),
    )

    assert select_flow("O que é o padrão Iterator?", Settings()) is Flow.CONCEPT


def test_example_question_uses_example_flow() -> None:
    assert select_flow("Mostre um exemplo em Java") is Flow.EXAMPLE


def test_diagnostic_question_uses_diagnostic_flow() -> None:
    assert select_flow("Onde eu errei?") is Flow.DIAGNOSTIC


def test_greeting_and_fabrication_are_handled_without_agents(monkeypatch) -> None:
    monkeypatch.setattr(
        "agente.system.run_crew",
        lambda *args: (_ for _ in ()).throw(AssertionError()),
    )
    system = TutorSystem(Settings())

    greeting = system.answer("Olá")
    refusal = system.answer("Invente um fato falso sobre Iterator")

    assert "tutor" in greeting.casefold()
    assert "inventar" in refusal.casefold()


def test_system_keeps_reviewed_answer_in_memory(monkeypatch) -> None:
    monkeypatch.setattr("agente.system.select_flow", lambda *args: Flow.CONCEPT)
    monkeypatch.setattr(
        "agente.system.run_crew",
        lambda config, question, flow, context: "resposta revisada",
    )
    system = TutorSystem(Settings())

    system.answer("Primeira pergunta")
    system.answer("Segunda pergunta")

    assert "Primeira pergunta" in system.memory.format_context()
