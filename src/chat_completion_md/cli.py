import sys
from pathlib import Path

from chat_completion_md import json_to_md, md_to_json


def main() -> None:
    """CLI entrypoint for chat-completion-md.

    Convert between JSON and Markdown formats for chat completion requests:
    - If input is a JSON file, outputs markdown to stdout
    - If input is a Markdown file, outputs JSON to stdout
    """
    if len(sys.argv) != 2:
        print("Usage: chat_completion_md <file>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File {file_path} not found", file=sys.stderr)
        sys.exit(1)

    try:
        content = file_path.read_text()
        if file_path.suffix == ".json":
            print(json_to_md(content))
        elif file_path.suffix == ".md":
            print(md_to_json(content))
        else:
            print(f"Error: Unsupported file type {file_path.suffix}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
