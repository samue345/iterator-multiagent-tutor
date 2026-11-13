from types import SimpleNamespace

from agente import crew
from agente.config import Settings
from agente.router import Flow


class FakeCrew:
    def kickoff(self):
        return SimpleNamespace(raw="resposta revisada")


def test_run_crew_returns_raw_result(monkeypatch) -> None:
    monkeypatch.setattr(crew, "create_crew", lambda *args: FakeCrew())

    result = crew.run_crew(Settings(), "Explique Iterator", Flow.CONCEPT)

    assert result == "resposta revisada"


def test_run_crew_returns_plain_result_without_raw(monkeypatch) -> None:
    class PlainCrew:
        def kickoff(self):
            return "resposta simples"

    monkeypatch.setattr(crew, "create_crew", lambda *args: PlainCrew())

    assert crew.run_crew(Settings(), "Explique Iterator", Flow.CONCEPT) == (
        "resposta simples"
    )
