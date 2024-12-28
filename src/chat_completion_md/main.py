import json

import yaml
from pydantic import ValidationError

from chat_completion_md.types import LLMRequestConfig, Message


def json_to_md(json_str: str) -> str:
    """Convert JSON to Markdown.

    Convert a JSON string which contains the data for performing a request to
    OpenAI's chat completion API to a markdown formatted string.

    Args:
        json_str (str): JSON string.

    Returns:
        str : Markdown string.

    Raises:
        ValidationError: If the JSON structure is invalid.
        JSONDecodeError: If the JSON string cannot be decoded.
        KeyError: If the required 'messages' key is not found in the JSON.
    """
    llm_request_config = json.loads(json_str)
    try:
        messages = llm_request_config.pop("messages")
    except KeyError as e:
        raise KeyError("Messages key not found in JSON") from e
    try:
        messages = [Message.model_validate(msg) for msg in messages]
    except ValidationError as e:
        raise e
    try:
        llm_request_config = LLMRequestConfig.model_validate(llm_request_config)
    except ValidationError as e:
        raise e

    s = ""
    metadata = yaml.dump(llm_request_config.model_dump(exclude_none=True)).strip()
    s += "---\n" + rf"{metadata}" + "\n---\n"
    for message in messages:
        s += f"\n# {message.role}\n"
        s += f"\n{message.content}\n"
        s += "\n---\n"

    return s


def md_to_json(md_str: str) -> str: ...
