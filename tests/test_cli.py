import sys

from agente import __main__
from agente.system import InvalidTutorResponseError, TutorExecutionError


class FakeSystem:
    def __init__(self, answer: str = "resposta") -> None:
        self.answer_text = answer
        self.questions: list[str] = []

    def answer(self, question: str) -> str:
        self.questions.append(question)
        return self.answer_text


def test_single_question_cli(monkeypatch, capsys) -> None:
    system = FakeSystem()
    monkeypatch.setattr(__main__, "TutorSystem", lambda: system)
    monkeypatch.setattr(sys, "argv", ["agente", "Explique", "Iterator"])

    assert __main__.main() == 0
    assert system.questions == ["Explique Iterator"]
    assert "resposta" in capsys.readouterr().out


def test_interactive_cli_stops_with_exit_command(monkeypatch, capsys) -> None:
    system = FakeSystem()
    answers = iter(["Explique Iterator", "sair"])
    monkeypatch.setattr(__main__, "TutorSystem", lambda: system)
    monkeypatch.setattr(sys, "argv", ["agente"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert __main__.main() == 0
    assert system.questions == ["Explique Iterator"]
    assert "Sistema: resposta" in capsys.readouterr().out


def test_cli_formats_known_errors(capsys) -> None:
    assert "Erro:" in __main__._user_facing_error(TutorExecutionError("falha"))
    assert "Erro:" in __main__._user_facing_error(
        InvalidTutorResponseError("resposta inválida")
    )
