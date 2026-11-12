from crewai import Agent, Task


def _context_text(context: str) -> str:
    if not context.strip():
        return "Sem histórico anterior nesta sessão."
    return (
        "Histórico anterior desta sessão (respostas finais revisadas; use como "
        "contexto e confira a correção antes de reutilizar):\n"
        f"{context}"
    )


def create_concept_task(question: str, agent: Agent, context: str = "") -> Task:
    return Task(
        description=(
            "Explique conceitualmente o padrão Iterator e responda à pergunta "
            f"do estudante:\n\n{question}\n\n{_context_text(context)}"
        ),
        expected_output="Explicação correta, clara e concisa em português.",
        agent=agent,
    )


def create_example_task(question: str, agent: Agent, context: str = "") -> Task:
    return Task(
        description=(
            "Produza um exemplo pequeno e correto do padrão Iterator para a "
            f"pergunta abaixo:\n\n{question}\n\n{_context_text(context)}"
        ),
        expected_output="Exemplo correto, explicado em português, sem detalhes inventados.",
        agent=agent,
    )


def create_diagnostic_task(question: str, agent: Agent, context: str = "") -> Task:
    return Task(
        description=(
            "Analise a dúvida ou tentativa do estudante e forneça uma orientação "
            f"pedagógica:\n\n{question}\n\n{_context_text(context)}"
        ),
        expected_output="Diagnóstico pedagógico e próxima pista em português.",
        agent=agent,
    )


def create_review_task(
    question: str,
    agent: Agent,
    context: list[Task],
    conversation_context: str = "",
) -> Task:
    return Task(
        description=(
            "Revise as respostas produzidas para a pergunta abaixo. Corrija "
            "imprecisões, remova invenções e consolide uma resposta final clara. "
            f"Pergunta do estudante:\n\n{question}\n\n"
            f"{_context_text(conversation_context)}"
        ),
        expected_output="Uma única resposta final correta e pedagógica em português.",
        agent=agent,
        context=context,
    )
