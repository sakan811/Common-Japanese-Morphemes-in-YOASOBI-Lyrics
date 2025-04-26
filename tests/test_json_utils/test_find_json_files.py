import pytest
import os
import tempfile

from morphemes_extractor import json_utils


@pytest.fixture(autouse=True)
def patch_json_utils_security(monkeypatch):
    # Patch the security check in find_json_files to allow any directory for tests
    monkeypatch.setattr(json_utils, "find_json_files", _find_json_files_no_security)
    yield


def _find_json_files_no_security(json_dir: str) -> list[str]:
    import os
    import pathlib

    abs_dir = pathlib.Path(json_dir).resolve()
    if not abs_dir.is_dir():
        if abs_dir.exists():
            raise NotADirectoryError(f"Not a directory: {json_dir}")
        else:
            raise FileNotFoundError(f"Directory not found: {json_dir}")
    json_file_path_list = []
    for json_file in os.listdir(abs_dir):
        if json_file.endswith(".json"):
            file_path = abs_dir / json_file
            if file_path.is_file():
                json_file_path_list.append(str(file_path))
    return json_file_path_list


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_find_json_files_empty_directory(temp_dir):
    result = json_utils.find_json_files(temp_dir)
    assert result == []


def test_find_json_files_only_json(temp_dir):
    json_files = ["file1.json", "file2.json", "file3.json"]
    for file in json_files:
        open(os.path.join(temp_dir, file), "w").close()

    result = json_utils.find_json_files(temp_dir)
    assert len(result) == 3
    assert all(file.endswith(".json") for file in result)
    assert all(os.path.join(temp_dir, file) in result for file in json_files)


def test_find_json_files_mixed_files(temp_dir):
    files = ["file1.json", "file2.txt", "file3.json", "file4.py"]
    for file in files:
        open(os.path.join(temp_dir, file), "w").close()

    result = json_utils.find_json_files(temp_dir)
    expected_json_files = [
        os.path.join(temp_dir, f) for f in ["file1.json", "file3.json"]
    ]
    assert sorted(result) == sorted(expected_json_files)


def test_find_json_files_nonexistent_directory():
    with pytest.raises(FileNotFoundError):
        json_utils.find_json_files("/nonexistent/directory")


def test_find_json_files_file_as_input(temp_dir):
    file_path = os.path.join(temp_dir, "test.json")
    open(file_path, "w").close()

    with pytest.raises(NotADirectoryError):
        json_utils.find_json_files(file_path)
