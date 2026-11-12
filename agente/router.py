from dataclasses import dataclass
from enum import StrEnum
import re
from re import Pattern

from .config import Settings, settings
from .llm import create_llm


class Flow(StrEnum):
    GREETING = "greeting"
    REFUSAL = "refusal"
    CONCEPT = "concept"
    EXAMPLE = "example"
    DIAGNOSTIC = "diagnostic"


@dataclass(frozen=True)
class RouteRule:
    flow: Flow
    patterns: tuple[Pattern[str], ...]


EXPLICIT_RULES = (
    RouteRule(
        flow=Flow.EXAMPLE,
        patterns=(
            re.compile(
                r"\b(?:me )?(?:d[eê]|mostre|fa[cç]a|gere|crie|apresente)"
                r".{0,40}\b(?:um )?(?:exemplo|amostra|demonstra[cç][aã]o)\b"
            ),
            re.compile(
                r"\b(?:mostre|gere|escreva|crie).{0,40}"
                r"\b(?:c[oó]digo|implementa[cç][aã]o)\b"
            ),
        ),
    ),
    RouteRule(
        flow=Flow.DIAGNOSTIC,
        patterns=(
            re.compile(r"\b(?:onde|em que parte) (?:eu )?(?:errei|falhei)\b"),
            re.compile(
                r"\b(?:corrija|avalie|analise) (?:minha|a minha) resposta\b"
            ),
            re.compile(
                r"\b(?:tentei|respondi) .{0,40}"
                r"\b(?:est[aá]|est[aá] correto)\b"
            ),
        ),
    ),
)

SEMANTIC_PROMPT = (
    "Classifique a intenção da pergunta em exatamente uma palavra: "
    "concept, example ou diagnostic. "
    "Use example para pedidos de exemplo, amostra, demonstração ou código. "
    "Use diagnostic para exercícios, tentativas ou pedidos de correção. "
    "Use concept para explicações, definições, comparações e dúvidas gerais. "
    "Pergunta: {question}\nResposta:"
)

GREETING_PATTERNS = (
    re.compile(
        r"^(?:oi+|ol[áa]|e a[ií]|bom dia|boa tarde|boa noite|tudo bem|"
        r"como (?:vai|voc[eê] est[aá]))[!?., ]*$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^(?:oi+|ol[áa]|e a[ií]|bom dia|boa tarde|boa noite)[,. ]+"
        r"(?:tudo bem|como (?:vai|voc[eê] est[aá]))[!?., ]*$",
        re.IGNORECASE,
    ),
)

FABRICATION_PATTERNS = (
    re.compile(
        r"\b(?:invent\w*|fabric\w*|make up)\b.{0,80}"
        r"\b(?:padr[aã]o|fato|informa[cç][aã]o|participante|consequ[eê]ncia|"
        r"pattern|fact|information|participant|consequence)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:crie|criar|create)\b.{0,60}"
        r"\b(?:falso|falsa|fict[ií]cio|fict[ií]cia|inexistente|fake|"
        r"fictional|nonexistent)\b",
        re.IGNORECASE,
    ),
)


def _normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def _is_greeting(question: str) -> bool:
    normalized = _normalize(question)
    return any(pattern.fullmatch(normalized) for pattern in GREETING_PATTERNS)


def _is_fabrication_request(question: str) -> bool:
    normalized = _normalize(question)
    for pattern in FABRICATION_PATTERNS:
        match = pattern.search(normalized)
        if match is None:
            continue
        prefix = normalized[max(0, match.start() - 40) : match.start()]
        if re.search(
            r"\b(?:n[aã]o|nunca|never|don't|do not)(?:\s+\w+){0,2}\s*$",
            prefix,
        ):
            continue
        return True
    return False


def _matches_rule(rule: RouteRule, question: str) -> bool:
    return any(pattern.search(question) for pattern in rule.patterns)


def _select_explicit_flow(question: str) -> Flow | None:
    normalized = _normalize(question)
    matching_rule = next(
        (rule for rule in EXPLICIT_RULES if _matches_rule(rule, normalized)),
        None,
    )
    return matching_rule.flow if matching_rule else None


def _select_semantic_flow(question: str, config: Settings) -> Flow:
    prompt = SEMANTIC_PROMPT.format(question=question)
    response = create_llm(config).call([{"role": "user", "content": prompt}])
    decision = re.search(
        r"\b(concept|example|diagnostic)\b",
        str(response).casefold(),
    )
    return Flow(decision.group(1)) if decision else Flow.CONCEPT


def select_flow(question: str, config: Settings = settings) -> Flow:
    if _is_greeting(question):
        return Flow.GREETING
    if _is_fabrication_request(question):
        return Flow.REFUSAL
    explicit_flow = _select_explicit_flow(question)
    return explicit_flow or _select_semantic_flow(question, config)
