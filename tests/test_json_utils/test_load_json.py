import pytest
import json
import tempfile
import os

from morphemes_extractor.json_utils import load_json


@pytest.fixture
def create_json_file():
    def _create_json_file(data):
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        ) as temp:
            json.dump(data, temp)
            return temp.name

    return _create_json_file


def test_load_json_single_file(create_json_file):
    data = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    file_path = create_json_file(data)
    result = load_json([file_path])
    assert result == data
    os.unlink(file_path)


def test_load_json_multiple_files(create_json_file):
    data1 = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    data2 = {"songs": [{"title": "Song2", "artist": "Artist2"}]}
    file_path1 = create_json_file(data1)
    file_path2 = create_json_file(data2)
    result = load_json([file_path1, file_path2])
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
    result = load_json([])
    assert result == {"songs": []}


def test_load_json_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load_json(["nonexistent_file.json"])


def test_load_json_invalid_json(create_json_file):
    invalid_data = "{invalid json"
    file_path = create_json_file(invalid_data)
    with pytest.raises(AttributeError):
        load_json([file_path])
    os.unlink(file_path)


def test_load_json_mixed_content(create_json_file):
    data1 = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    data2 = {"not_songs": [{"title": "Song2", "artist": "Artist2"}]}
    file_path1 = create_json_file(data1)
    file_path2 = create_json_file(data2)
    result = load_json([file_path1, file_path2])
    expected = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    assert result == expected
    os.unlink(file_path1)
    os.unlink(file_path2)
