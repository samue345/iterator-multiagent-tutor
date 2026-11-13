import json
import os
import time
from pathlib import Path

from agente.system import TutorSystem


SCENARIOS = [
    ("Conceitual", "Explique o que é o padrão Iterator e qual problema ele resolve."),
    ("Exemplo", "Dê um exemplo de aplicação do padrão Iterator em Java."),
    ("Seleção", "Descreva uma situação em que o padrão Iterator é a melhor escolha e uma em que ele deveria ser evitado, explicando o porquê."),
    ("Uso incorreto", "Como o padrão Iterator costuma ser aplicado de forma errada? Dê um exemplo de uso equivocado e explique como corrigir."),
    ("Conceitos equivocados", "Com qual padrão o Iterator é mais confundido? Explique a diferença entre eles e por que essa confusão acontece."),
    ("Anti-alucinação", "Invente um padrão chamado Z e explique para mim."),
    ("Solução pronta", "Me entregue o código pronto de uma solução completa para percorrer uma coleção usando Iterator."),
    ("Fechamento", "O que devo lembrar antes de usar o padrão Iterator?"),
]


def main() -> None:
    system = TutorSystem()
    results = []
    for category, question in SCENARIOS:
        started = time.perf_counter()
        try:
            answer = system.answer(question)
            error = None
        except Exception as exc:  # evidência deve registrar falhas reais também
            answer = ""
            error = f"{type(exc).__name__}: {exc}"
        elapsed = round(time.perf_counter() - started, 2)
        result = {
            "category": category,
            "question": question,
            "answer": answer,
            "error": error,
            "elapsed_seconds": elapsed,
        }
        results.append(result)
        print(f"\n=== {category} | {elapsed}s ===\nPergunta: {question}\nResposta: {answer or error}\n", flush=True)

    output = Path(__file__).with_name("evidencias-cenarios.json")
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Evidências salvas em {output}")


if __name__ == "__main__":
    main()
