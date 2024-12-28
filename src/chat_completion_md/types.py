from typing import Literal
from pydantic import BaseModel, ConfigDict


class LLMRequestConfig(BaseModel):
    model: str
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None
    stream: bool | None = None
    # stop: str | list[str] | None = None # Not supported to avoid parkur escaping
    presence_penalty: float | None = None
    frequency_penalty: float | None = None
    logit_bias: dict[str, int] | None = None


class Message(BaseModel):
    model_config = ConfigDict(extra="allow")
    role: Literal["system", "user", "assistant", "developer", "tool"]
    content: str
