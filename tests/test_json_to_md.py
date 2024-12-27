import json
import pytest
from pathlib import Path
from chat_completion_md import json_to_md

here = Path(__file__).parent
json_flies: list[Path] = sorted((here / "data" / "json_to_md").glob("*.json"))
md_flies: list[Path] = sorted((here / "data" / "json_to_md").glob("*.md"))


@pytest.mark.parametrize("json_file, md_file", zip(json_flies, md_flies))
def test_json_to_md(json_file, md_file):
    json_str = json.loads(json_file.read_text())
    md_str = md_file.read_text()
    output = json_to_md(json_str)
    assert output == md_str
