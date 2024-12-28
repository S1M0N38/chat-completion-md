import json
import re

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


def md_to_json(md_str: str) -> str:
    """Convert Markdown to JSON.

    Convert a Markdown string (formatted according to the defined
    specification) to a JSON string for performing a request to OpenAI's chat
    completion API.

    Args:
        md_str (str): Markdown string.

    Returns:
        str : JSON string.

    Raises:
        ValueError: If the Markdown string is not properly formatted or
            messages are missing.
        KeyError: If the required keys are not found in the front matter.
    """
    pattern = r"\A---\n(.*?)\n---\n(.*)"
    match = re.search(pattern, md_str, re.DOTALL)
    if match is None:
        raise ValueError("Cannot parse Markdown string")

    yaml_str = match.group(1)
    if not yaml_str:
        raise ValueError("Front matter is empty")
    llm_request_config = yaml.safe_load(yaml_str)

    if "model" not in llm_request_config:
        raise KeyError("Model key not found in front matter")

    msgs_str = match.group(2)
    if not msgs_str:
        raise ValueError("Content after front matter is empty")

    roles = ["system", "user", "assistant", "developer", "tool"]
    pattern = (
        rf"\n# ({'|'.join(roles)})\n\n"
        rf"(.*?)\n\n---(?=(?:\n\n# (?:{'|'.join(roles)})\n\n|\s*\Z))"
    )

    messages = [
        {"role": match.group(1), "content": match.group(2)}
        for match in re.finditer(pattern, msgs_str, re.DOTALL)
    ]

    if not messages:
        raise ValueError("No messages found")

    json_str = json.dumps(
        {**llm_request_config, "messages": messages},
        indent=2,
        sort_keys=True,
    )
    return json_str
