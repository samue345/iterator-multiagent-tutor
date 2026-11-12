import sys

from .system import InvalidTutorResponseError, TutorExecutionError, TutorSystem


def _user_facing_error(exc: Exception) -> str:
    message = str(exc)
    if isinstance(exc, (TutorExecutionError, InvalidTutorResponseError)):
        return f"Erro: {message}"
    if isinstance(exc, RuntimeError) and message.startswith(
        ("Ollama está indisponível.", "Ollama respondeu com status HTTP")
    ):
        return f"Erro: {message}"
    return (
        "Erro: não foi possível gerar uma resposta. Verifique se o Ollama está "
        "em execução e se o modelo configurado está disponível; depois tente "
        "novamente."
    )


def _answer(system: TutorSystem, question: str, prefix: str = "") -> bool:
    try:
        answer = system.answer(question)
    except Exception as exc:
        print(_user_facing_error(exc), file=sys.stderr)
        return False
    print(f"{prefix}{answer}")
    return True


def main() -> int:
    system = TutorSystem()

    if len(sys.argv) > 1:
        return 0 if _answer(system, " ".join(sys.argv[1:])) else 1

    print("Tutor Iterator. Digite 'sair' para encerrar.")
    while True:
        try:
            question = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if question.lower() in {"sair", "exit", "quit"}:
            break
        _answer(system, question, prefix="Sistema: ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
