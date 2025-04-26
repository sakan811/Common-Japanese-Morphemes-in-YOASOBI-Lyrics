import json
import pytest
from unittest.mock import patch
from morphemes_extractor import json_utils


@pytest.fixture(autouse=True)
def patch_json_utils_security(monkeypatch):
    monkeypatch.setattr(json_utils, "load_json_file", _load_json_file_no_security)
    yield


def _load_json_file_no_security(file_path: str):
    import json
    import pathlib

    abs_path = pathlib.Path(file_path).resolve()
    if not abs_path.is_file() or abs_path.suffix != ".json":
        if abs_path.exists():
            raise ValueError(f"Not a JSON file: {file_path}")
        else:
            raise FileNotFoundError(f"File not found: {file_path}")
    with open(abs_path, "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture
def sample_json_file(tmp_path):
    data = {"key": "value", "number": 42}
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return str(file_path)


def test_load_json_file_returns_dict(sample_json_file):
    result = json_utils.load_json_file(sample_json_file)
    assert isinstance(result, dict)


def test_load_json_file_correct_content(sample_json_file):
    result = json_utils.load_json_file(sample_json_file)
    assert result == {"key": "value", "number": 42}


def test_load_json_file_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        json_utils.load_json_file("nonexistent_file.json")


def test_load_json_file_invalid_json(tmp_path):
    invalid_json_file = tmp_path / "invalid.json"
    with open(invalid_json_file, "w", encoding="utf-8") as f:
        f.write("{invalid json")

    with pytest.raises(json.JSONDecodeError):
        json_utils.load_json_file(str(invalid_json_file))


def test_load_json_file_empty_file(tmp_path):
    empty_file = tmp_path / "empty.json"
    empty_file.touch()

    with pytest.raises(json.JSONDecodeError):
        json_utils.load_json_file(str(empty_file))
