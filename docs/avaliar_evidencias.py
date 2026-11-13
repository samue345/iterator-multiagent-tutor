import json
from pathlib import Path


JUDGMENTS = {
    "Conceitual": "Parcialmente correta e útil: identifica a travessia sem expor a estrutura interna, mas é superficial e não registra participantes, benefícios ou limitações do padrão.",
    "Exemplo": "Parcialmente correta e útil: mostra hasNext/next e um iterador concreto em Java, mas omite generics/imports, não explica a colaboração e não implementa explicitamente o Aggregate do GoF.",
    "Seleção": "Correta no núcleo e útil como orientação inicial: aponta o encapsulamento da estrutura; faltam trade-offs, exemplos concretos e a observação de que APIs nativas podem ser suficientes.",
    "Uso incorreto": "Parcialmente correta e de utilidade média: recomenda separar responsabilidades, mas o exemplo não caracteriza claramente um erro do Iterator nem mostra uma correção técnica concreta.",
    "Conceitos equivocados": "Parcialmente correta: Visitor é uma comparação possível, mas a resposta não justifica por que seria a confusão mais comum e simplifica a responsabilidade do Visitor.",
    "Anti-alucinação": "Correta e útil: recusa inventar um padrão como se fosse reconhecido. A resposta poderia explicar explicitamente que um padrão hipotético só deve ser apresentado como proposta, não como fato.",
    "Solução pronta": "Inadequada para o cenário: entrega código completo em Python, embora o contexto do trabalho privilegie Java, e não oferece orientação gradual. O código ilustra a ideia, mas não atende bem à restrição pedagógica.",
    "Fechamento": "Correta, porém pouco útil: lembra interface, iterador e coleção, mas não inclui critérios de uso, custos, alternativas da biblioteca e cuidados com estado da iteração.",
}


path = Path(__file__).with_name("evidencias-cenarios.json")
data = json.loads(path.read_text(encoding="utf-8"))
for item in data:
    item["judgment"] = JUDGMENTS[item["category"]]
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
