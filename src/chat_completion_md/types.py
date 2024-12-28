from typing import Literal
from pydantic import BaseModel, ConfigDict


class LLMRequestConfig(BaseModel):
    frequency_penalty: float | None = None
    logit_bias: dict[str, int] | None = None
    max_tokens: int | None = None
    model: str
    presence_penalty: float | None = None
    stream: bool | None = None
    temperature: float | None = None
    top_p: float | None = None


class Message(BaseModel):
    model_config = ConfigDict(extra="allow")
    content: str
    role: Literal["assistant", "developer", "system", "tool", "user"]
