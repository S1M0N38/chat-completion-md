import json
from pathlib import Path

import pytest

from chat_completion_md import md_to_json

here = Path(__file__).parent

class TestMdToJson:
    data_path = here / "data" / "md_to_json"
    example_mds: list[Path] = sorted(data_path.glob("example_*.md"))
    example_jsons: list[Path] = sorted(data_path.glob("example_*.json"))

    @pytest.mark.parametrize("md_file, json_file", zip(example_mds, example_jsons))
    def test_md_to_json(self, md_file, json_file):
        md_str = md_file.read_text()
        json_str = json_file.read_text()
        output = md_to_json(md_str)
        assert json.loads(output) == json.loads(json_str)

    def test_not_valid_markdown(self):
        md_str = (self.data_path / "not_valid_markdown.md").read_text()
        with pytest.raises(ValueError) as e:
           md_to_json(md_str)
        assert "Cannot parse Markdown string" in str(e.value)

    def test_missing_model(self):
        md_str = (self.data_path / "missing_model.md").read_text()
        with pytest.raises(KeyError) as e:
            md_to_json(md_str)
        assert "Model key not found in front matter" in str(e.value)

    def test_missing_content(self):
        md_str = (self.data_path / "missing_content.md").read_text()
        with pytest.raises(ValueError) as e:
            md_to_json(md_str)
        assert "Content after front matter is empty" in str(e.value)

    def test_missing_messages(self):
        md_str = (self.data_path / "missing_messages.md").read_text()
        with pytest.raises(ValueError) as e:
            md_to_json(md_str)
        assert "No messages found" in str(e.value)
