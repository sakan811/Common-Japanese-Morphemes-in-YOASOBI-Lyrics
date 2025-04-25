import pytest
import os
import tempfile

from morphemes_extractor.json_utils import find_json_files


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_find_json_files_empty_directory(temp_dir):
    result = find_json_files(temp_dir)
    assert result == []


def test_find_json_files_only_json(temp_dir):
    json_files = ["file1.json", "file2.json", "file3.json"]
    for file in json_files:
        open(os.path.join(temp_dir, file), "w").close()

    result = find_json_files(temp_dir)
    assert len(result) == 3
    assert all(file.endswith(".json") for file in result)
    assert all(os.path.join(temp_dir, file) in result for file in json_files)


def test_find_json_files_mixed_files(temp_dir):
    files = ["file1.json", "file2.txt", "file3.json", "file4.py"]
    for file in files:
        open(os.path.join(temp_dir, file), "w").close()

    result = find_json_files(temp_dir)
    assert len(result) == 4  # All files are included, not just .json
    assert all(os.path.join(temp_dir, file) in result for file in files)


def test_find_json_files_nonexistent_directory():
    with pytest.raises(FileNotFoundError):
        find_json_files("/nonexistent/directory")


def test_find_json_files_file_as_input(temp_dir):
    file_path = os.path.join(temp_dir, "test.json")
    open(file_path, "w").close()

    with pytest.raises(NotADirectoryError):
        find_json_files(file_path)
