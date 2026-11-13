import pytest

from agente.contracts import AgentResponse, TutorRequest
from agente.system import InvalidTutorResponseError, _validate_response


@pytest.mark.parametrize("response", [None, "", "  ", "none", "null", "[]", "{}"])
def test_invalid_responses_are_rejected(response: object) -> None:
    with pytest.raises(InvalidTutorResponseError):
        _validate_response(response)


def test_valid_response_is_trimmed() -> None:
    assert _validate_response("  resposta válida  ") == "resposta válida"


def test_contracts_require_non_empty_content() -> None:
    with pytest.raises(ValueError):
        TutorRequest(question="")
    with pytest.raises(ValueError):
        AgentResponse(agent_name="revisor", content="")
