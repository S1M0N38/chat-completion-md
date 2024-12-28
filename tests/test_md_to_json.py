import json
import pytest
from pathlib import Path
from chat_completion_md import md_to_json

here = Path(__file__).parent
example_mds: list[Path] = sorted((here / "data" / "md_to_json").glob("example_*.md"))
example_jsons: list[Path] = sorted((here / "data" / "md_to_json").glob("example_*.json"))


@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.parametrize("md_file, json_file", zip(example_mds, example_jsons))
def test_md_to_json(md_file, json_file):
    md_str = md_file.read_text()
    json_str = json.loads(json_file.read_text())
    output = md_to_json(md_str)
    assert output == json_str
