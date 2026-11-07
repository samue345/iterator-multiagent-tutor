import sys

from .system import TutorSystem


def main() -> None:
    system = TutorSystem()

    if len(sys.argv) > 1:
        print(system.answer(" ".join(sys.argv[1:])))
        return

    print("Tutor Iterator. Digite 'sair' para encerrar.")
    while True:
        try:
            question = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if question.lower() in {"sair", "exit", "quit"}:
            break
        print(f"Sistema: {system.answer(question)}")


if __name__ == "__main__":
    main()
