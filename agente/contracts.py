from pydantic import BaseModel, ConfigDict, Field


class TutorRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    question: str = Field(min_length=1)
    previous_context: str = ""


class AgentResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    agent_name: str = Field(min_length=1)
    content: str = Field(min_length=1)
