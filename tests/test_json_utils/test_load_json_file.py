import json

import pytest

from morphemes_extractor.json_utils import load_json_file


@pytest.fixture
def sample_json_file(tmp_path):
    data = {"key": "value", "number": 42}
    file_path = tmp_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return str(file_path)


def test_load_json_file_returns_dict(sample_json_file):
    result = load_json_file(sample_json_file)
    assert isinstance(result, dict)


def test_load_json_file_correct_content(sample_json_file):
    result = load_json_file(sample_json_file)
    assert result == {"key": "value", "number": 42}


def test_load_json_file_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load_json_file("nonexistent_file.json")


def test_load_json_file_invalid_json(tmp_path):
    invalid_json_file = tmp_path / "invalid.json"
    with open(invalid_json_file, "w", encoding="utf-8") as f:
        f.write("{invalid json")

    with pytest.raises(json.JSONDecodeError):
        load_json_file(str(invalid_json_file))


def test_load_json_file_empty_file(tmp_path):
    empty_file = tmp_path / "empty.json"
    empty_file.touch()

    with pytest.raises(json.JSONDecodeError):
        load_json_file(str(empty_file))
