from crewai import Agent, Task


def create_concept_task(question: str, agent: Agent, context: str = "") -> Task:
    return Task(
        description=(
            "Explique conceitualmente o padrão Iterator e responda à pergunta "
            f"do estudante:\n\n{question}\n\nContexto anterior:\n{context}"
        ),
        expected_output="Explicação correta, clara e concisa em português.",
        agent=agent,
    )


def create_example_task(question: str, agent: Agent, context: str = "") -> Task:
    return Task(
        description=(
            "Produza um exemplo pequeno e correto do padrão Iterator para a "
            f"pergunta abaixo:\n\n{question}\n\nContexto anterior:\n{context}"
        ),
        expected_output="Exemplo correto, explicado em português, sem detalhes inventados.",
        agent=agent,
    )


def create_diagnostic_task(question: str, agent: Agent, context: str = "") -> Task:
    return Task(
        description=(
            "Analise a dúvida ou tentativa do estudante e forneça uma orientação "
            f"pedagógica:\n\n{question}\n\nContexto anterior:\n{context}"
        ),
        expected_output="Diagnóstico pedagógico e próxima pista em português.",
        agent=agent,
    )


def create_review_task(question: str, agent: Agent, context: list[Task]) -> Task:
    return Task(
        description=(
            "Revise as respostas produzidas para a pergunta abaixo. Corrija "
            "imprecisões, remova invenções e consolide uma resposta final clara. "
            f"Pergunta do estudante:\n\n{question}"
        ),
        expected_output="Uma única resposta final correta e pedagógica em português.",
        agent=agent,
        context=context,
    )
