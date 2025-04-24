from unittest.mock import patch

import pandas as pd
import pytest

from main import main


@pytest.fixture
def mock_json_files():
    return ["file1.json", "file2.json"]


@pytest.fixture
def mock_dataframe():
    return pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})


def test_main_successful_execution(mock_json_files, mock_dataframe):
    with (
        patch("main.find_json_files") as mock_find_json_files,
        patch("main.get_morphemes_from_songs") as mock_get_morphemes,
        patch("main.save_to_db") as mock_save_to_sqlite,
    ):
        mock_find_json_files.return_value = mock_json_files
        mock_get_morphemes.return_value = mock_dataframe

        main("test.db", "test_dir")

        mock_find_json_files.assert_called_once_with("test_dir")
        mock_get_morphemes.assert_called_once_with(mock_json_files)
        mock_save_to_sqlite.assert_called_once_with(mock_dataframe, "test.db")


def test_main_no_json_files():
    with (
        patch("main.find_json_files") as mock_find_json_files,
        patch("main.get_morphemes_from_songs") as mock_get_morphemes,
        patch("main.save_to_db") as mock_save_to_sqlite,
        patch("main.logger.warning") as mock_logger_warning,
    ):
        mock_find_json_files.return_value = []

        main("test.db", "empty_dir")

        mock_find_json_files.assert_called_once_with("empty_dir")
        mock_get_morphemes.assert_not_called()
        mock_save_to_sqlite.assert_not_called()
        mock_logger_warning.assert_called_once_with(
            "No JSON files found in the specified directory."
        )


def test_main_empty_dataframe(mock_json_files):
    with (
        patch("main.find_json_files") as mock_find_json_files,
        patch("main.get_morphemes_from_songs") as mock_get_morphemes,
        patch("main.save_to_db") as mock_save_to_sqlite,
        patch("main.logger.warning") as mock_logger_warning,
    ):
        mock_find_json_files.return_value = mock_json_files
        mock_get_morphemes.return_value = pd.DataFrame()

        main("test.db", "test_dir")

        mock_find_json_files.assert_called_once_with("test_dir")
        mock_get_morphemes.assert_called_once_with(mock_json_files)
        mock_save_to_sqlite.assert_not_called()
        mock_logger_warning.assert_called_once_with(
            "No morphemes found in the JSON files."
        )
