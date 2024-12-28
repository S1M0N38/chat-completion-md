from json import JSONDecodeError
from pathlib import Path

import pytest
from pydantic import ValidationError

from chat_completion_md import json_to_md

here = Path(__file__).parent

class TestJsonToMd:

    data_path = here / "data" / "json_to_md"
    example_jsons: list[Path] = sorted(data_path.glob("example_*.json"))
    example_mds: list[Path] = sorted(data_path.glob("example_*.md"))


    @pytest.mark.parametrize("json_file, md_file", zip(example_jsons, example_mds))
    def test_examples(self, json_file, md_file):
        json_str = json_file.read_text()
        md_str = md_file.read_text()
        output = json_to_md(json_str)
        assert output == md_str

    def test_not_valid_json(self):
        json_str = (self.data_path / "not_valid_json.json").read_text()
        with pytest.raises(JSONDecodeError) as e:
            json_to_md(json_str)
        assert "Expecting property name enclosed in double quotes" in str(e.value)

    def test_missing_messages(self):
        json_str = (self.data_path / "missing_messages.json").read_text()
        with pytest.raises(KeyError) as e:
            json_to_md(json_str)
        assert "Messages key not found in JSON" in str(e.value)

    def test_missing_model(self):
        json_str = (self.data_path / "missing_model.json").read_text()
        with pytest.raises(ValidationError) as exc_info:
            json_to_md(json_str)
        errors = exc_info.value.errors()[0]
        assert "model" in errors["loc"]
        assert "Field required" == errors["msg"]

    def test_wrong_role(self):
        json_str = (self.data_path / "wrong_role.json").read_text()
        with pytest.raises(ValidationError) as exc_info:
            json_to_md(json_str)
        errors = exc_info.value.errors()[0]
        msg = "Input should be 'assistant', 'developer', 'system', 'tool' or 'user'"
        assert msg == errors["msg"]
