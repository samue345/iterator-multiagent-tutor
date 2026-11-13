from agente.memory import TutorMemory


def test_memory_keeps_only_recent_turns() -> None:
    memory = TutorMemory(max_turns=2)
    memory.add("primeira", "resposta 1")
    memory.add("segunda", "resposta 2")
    memory.add("terceira", "resposta 3")

    context = memory.format_context()

    assert "primeira" not in context
    assert "segunda" in context
    assert "terceira" in context


def test_memory_limits_context_size() -> None:
    memory = TutorMemory(max_context_chars=60)
    memory.add("pergunta", "resposta muito longa " * 20)

    assert len(memory.format_context()) <= 60


def test_memory_ignores_empty_turns() -> None:
    memory = TutorMemory()
    memory.add("", "resposta")
    memory.add("pergunta", "")

    assert memory.format_context() == ""
