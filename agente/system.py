from crewai import Crew, Process, Task

from .agents import create_concept_tutor
from .config import Settings, settings


class TutorSystem:
    """Implementação inicial usada para validar CrewAI e Ollama."""

    def __init__(self, config: Settings = settings) -> None:
        self.config = config
        self.concept_tutor = create_concept_tutor(config)

    def answer(self, question: str) -> str:
        if not question.strip():
            return "Escreva uma pergunta sobre o padrão Iterator."

        task = Task(
            description=(
                "Responda à pergunta abaixo como uma primeira explicação pedagógica "
                "sobre o padrão Iterator.\n\n"
                f"Pergunta do estudante: {question}"
            ),
            expected_output="Uma explicação correta, clara e concisa em português.",
            agent=self.concept_tutor,
        )
        crew = Crew(
            agents=[self.concept_tutor],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )
        return str(crew.kickoff())
