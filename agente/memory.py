from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationTurn:
    question: str
    reviewed_answer: str


class TutorMemory:
    """Histórico curto, em memória, limitado à vida de uma sessão do tutor."""

    def __init__(self, max_turns: int = 6, max_context_chars: int = 8_000) -> None:
        if max_turns < 1:
            raise ValueError("max_turns precisa ser maior que zero.")
        if max_context_chars < 1:
            raise ValueError("max_context_chars precisa ser maior que zero.")
        self.max_turns = max_turns
        self.max_context_chars = max_context_chars
        self._turns: list[ConversationTurn] = []

    def add(self, question: str, reviewed_answer: str) -> None:
        if not question.strip() or not reviewed_answer.strip():
            return
        self._turns.append(ConversationTurn(question, reviewed_answer))
        self._turns = self._turns[-self.max_turns :]

    def format_context(self) -> str:
        if not self._turns:
            return ""

        sections: list[str] = []
        for turn in reversed(self._turns):
            section = (
                f"Pergunta anterior: {turn.question}\n"
                f"Resposta final revisada: {turn.reviewed_answer}"
            )
            candidate = "\n\n".join([section, *sections])
            if len(candidate) > self.max_context_chars:
                if not sections:
                    available = self.max_context_chars - len(
                        "Pergunta anterior: \nResposta final revisada: "
                    )
                    if available > 0:
                        answer_limit = max(0, available - len(turn.question))
                        section = (
                            f"Pergunta anterior: {turn.question}\n"
                            "Resposta final revisada: "
                            f"{turn.reviewed_answer[:answer_limit]}"
                        )
                        sections.append(section[: self.max_context_chars])
                break
            sections.insert(0, section)

        return "\n\n".join(sections)
