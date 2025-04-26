import pytest
import json
import tempfile
import os
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
def create_json_file():
    def _create_json_file(data):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        ) as temp:
            if isinstance(data, str):
                temp.write(data)
            else:
                json.dump(data, temp)
            return temp.name

    return _create_json_file


def test_load_json_single_file(create_json_file):
    data = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    file_path = create_json_file(data)
    result = json_utils.load_json([file_path])
    assert result == data
    os.unlink(file_path)


def test_load_json_multiple_files(create_json_file):
    data1 = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    data2 = {"songs": [{"title": "Song2", "artist": "Artist2"}]}
    file_path1 = create_json_file(data1)
    file_path2 = create_json_file(data2)
    result = json_utils.load_json([file_path1, file_path2])
    expected = {
        "songs": [
            {"title": "Song1", "artist": "Artist1"},
            {"title": "Song2", "artist": "Artist2"},
        ]
    }
    assert result == expected
    os.unlink(file_path1)
    os.unlink(file_path2)


def test_load_json_empty_file_list():
    result = json_utils.load_json([])
    assert result == {"songs": []}


def test_load_json_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        json_utils.load_json(["nonexistent_file.json"])


def test_load_json_invalid_json(create_json_file):
    invalid_data = "{invalid json"
    file_path = create_json_file(invalid_data)
    with pytest.raises(json.JSONDecodeError):
        json_utils.load_json([file_path])
    os.unlink(file_path)


def test_load_json_mixed_content(create_json_file):
    data1 = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    data2 = {"not_songs": [{"title": "Song2", "artist": "Artist2"}]}
    file_path1 = create_json_file(data1)
    file_path2 = create_json_file(data2)
    result = json_utils.load_json([file_path1, file_path2])
    expected = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    assert result == expected
    os.unlink(file_path1)
    os.unlink(file_path2)
