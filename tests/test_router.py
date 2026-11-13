from agente.config import Settings
from agente.router import Flow, select_flow


class FakeLlm:
    def __init__(self, response: str) -> None:
        self.response = response

    def call(self, messages: list[dict[str, str]]) -> str:
        return self.response


def test_explicit_example_request_does_not_call_llm(monkeypatch) -> None:
    monkeypatch.setattr(
        "agente.router.create_llm",
        lambda config: (_ for _ in ()).throw(AssertionError()),
    )

    assert select_flow("Faça uma demonstração do Iterator") is Flow.EXAMPLE


def test_greeting_and_fabrication_are_routed_without_llm(monkeypatch) -> None:
    monkeypatch.setattr(
        "agente.router.create_llm",
        lambda config: (_ for _ in ()).throw(AssertionError()),
    )

    assert select_flow("Olá") is Flow.GREETING
    assert select_flow("Invente um padrão inexistente") is Flow.REFUSAL


def test_ambiguous_question_uses_semantic_router(monkeypatch) -> None:
    monkeypatch.setattr(
        "agente.router.create_llm",
        lambda config: FakeLlm("example"),
    )

    assert select_flow("Quero entender melhor essa parte", Settings()) is Flow.EXAMPLE


def test_invalid_semantic_response_falls_back_to_concept(monkeypatch) -> None:
    monkeypatch.setattr(
        "agente.router.create_llm",
        lambda config: FakeLlm("resultado inválido"),
    )

    assert select_flow("Explique essa dúvida", Settings()) is Flow.CONCEPT
