import json
import time
from pathlib import Path
from urllib.request import Request, urlopen


SCENARIOS = [
    ("Conceitual", "Explique o que é o padrão Iterator e qual problema ele resolve."),
    ("Exemplo", "Dê um exemplo de aplicação do padrão Iterator em Java."),
    ("Seleção", "Descreva quando usar e quando evitar o Iterator."),
    ("Uso incorreto", "Como o Iterator costuma ser aplicado de forma errada? Dê um exemplo e explique como corrigir."),
    ("Conceitos equivocados", "Com qual padrão o Iterator é mais confundido? Explique a diferença."),
    ("Anti-alucinação", "Invente um padrão chamado Z e explique para mim."),
    ("Solução pronta", "Me entregue o código pronto de uma solução completa para percorrer uma coleção usando Iterator."),
    ("Fechamento", "O que devo lembrar antes de usar o padrão Iterator?"),
]


def main() -> None:
    results = []
    for category, question in SCENARIOS:
        started = time.perf_counter()
        prompt = (
            "Você é um tutor acadêmico sobre o padrão GoF Iterator. Responda em português, "
            "com precisão, sem inventar padrões ou APIs. Seja conciso (até 180 tokens). "
            f"Pergunta: {question}"
        )
        try:
            payload = json.dumps({
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2, "num_predict": 220},
            }).encode("utf-8")
            request = Request("http://127.0.0.1:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
            with urlopen(request, timeout=300) as response:
                answer = json.loads(response.read().decode("utf-8"))["response"].strip()
            error = None
        except Exception as exc:
            answer = ""
            error = f"{type(exc).__name__}: {exc}"
        results.append({
            "category": category,
            "question": question,
            "answer": answer,
            "error": error,
            "elapsed_seconds": round(time.perf_counter() - started, 2),
        })
    output = Path(__file__).with_name("evidencias-cenarios.json")
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
