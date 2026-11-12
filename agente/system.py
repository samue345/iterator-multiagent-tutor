from .config import Settings, settings
from .crew import run_crew
from .memory import TutorMemory
from .router import Flow, select_flow


class TutorExecutionError(RuntimeError):
    """Falha compreensível durante a execução dos agentes do tutor."""


class InvalidTutorResponseError(RuntimeError):
    """A resposta final não contém conteúdo utilizável pelo estudante."""


def _validate_response(response: object) -> str:
    if not isinstance(response, str):
        raise InvalidTutorResponseError(
            "O tutor retornou uma resposta em formato inesperado. Tente novamente."
        )
    answer = response.strip()
    if answer.casefold() in {"", "none", "null", "[]", "{}"}:
        raise InvalidTutorResponseError(
            "O tutor retornou uma resposta vazia ou inválida. Tente novamente."
        )
    return answer


class TutorSystem:
    def __init__(self, config: Settings = settings) -> None:
        self.config = config
        self.memory = TutorMemory()

    def answer(self, question: str) -> str:
        if not question.strip():
            return "Escreva uma pergunta sobre o padrão Iterator."
        try:
            flow = select_flow(question, self.config)
        except RuntimeError as exc:
            if str(exc).startswith(
                ("Ollama está indisponível.", "Ollama respondeu com status HTTP")
            ):
                raise
            raise TutorExecutionError(
                "Os agentes não conseguiram concluir a resposta. Tente novamente."
            ) from exc
        except Exception as exc:
            raise TutorExecutionError(
                "Não foi possível classificar a pergunta. Tente novamente."
            ) from exc

        if flow is Flow.GREETING:
            return (
                "Olá! Estou bem, obrigado. Sou um tutor que ensina o padrão "
                "Iterator. Como posso ajudar você com esse padrão?"
            )
        if flow is Flow.REFUSAL:
            return (
                "Não vou inventar padrões, participantes ou fatos. Posso ajudar "
                "com informações confiáveis sobre o padrão Iterator."
            )
        context = self.memory.format_context()
        try:
            response = run_crew(self.config, question, flow, context)
        except RuntimeError as exc:
            if str(exc).startswith(
                ("Ollama está indisponível.", "Ollama respondeu com status HTTP")
            ):
                raise
            raise TutorExecutionError(
                "Os agentes não conseguiram concluir a resposta. Tente novamente."
            ) from exc
        except Exception as exc:
            raise TutorExecutionError(
                "Ocorreu uma falha durante a tarefa do tutor. Tente novamente."
            ) from exc

        answer = _validate_response(response)
        self.memory.add(question, answer)
        return answer
