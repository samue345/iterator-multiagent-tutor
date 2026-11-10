from .config import Settings, settings
from .crew import run_crew
from .router import select_flow


class TutorSystem:
    def __init__(self, config: Settings = settings) -> None:
        self.config = config

    def answer(self, question: str) -> str:
        if not question.strip():
            return "Escreva uma pergunta sobre o padrão Iterator."
        return run_crew(self.config, question, select_flow(question, self.config))
