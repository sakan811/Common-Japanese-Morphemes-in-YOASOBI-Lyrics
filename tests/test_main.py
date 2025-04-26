from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
import pytest

from main import app

client = TestClient(app)


@pytest.fixture
def mock_json_files():
    return ["file1.json", "file2.json"]


@pytest.fixture
def mock_dataframe():
    return pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})


def test_extract_morphemes_success(monkeypatch, mock_json_files, mock_dataframe):
    monkeypatch.setenv("DB_USER", "test")
    monkeypatch.setenv("DB_PASSWORD", "test")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("JSON_DIR", "test_dir")

    with (
        patch(
            "main.find_json_files", return_value=mock_json_files
        ) as mock_find_json_files,
        patch(
            "main.get_morphemes_from_songs", return_value=mock_dataframe
        ) as mock_get_morphemes,
        patch("main.save_to_db") as mock_save_to_db,
    ):
        response = client.post("/extract-morphemes/")
        assert response.status_code == 200
        assert (
            response.json()["message"] == "Morphemes extracted and saved to database."
        )
        mock_find_json_files.assert_called_once_with("test_dir")
        mock_get_morphemes.assert_called_once_with(mock_json_files)
        mock_save_to_db.assert_called_once_with(
            mock_dataframe, "postgresql://test:test@localhost:5432/testdb"
        )


def test_extract_morphemes_no_json_files(monkeypatch):
    monkeypatch.setenv("DB_USER", "test")
    monkeypatch.setenv("DB_PASSWORD", "test")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("JSON_DIR", "empty_dir")

    with patch("main.find_json_files", return_value=[]) as mock_find_json_files:
        response = client.post("/extract-morphemes/")
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "No JSON files found in the specified directory."
        )
        mock_find_json_files.assert_called_once_with("empty_dir")


def test_extract_morphemes_empty_dataframe(monkeypatch, mock_json_files):
    monkeypatch.setenv("DB_USER", "test")
    monkeypatch.setenv("DB_PASSWORD", "test")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("JSON_DIR", "test_dir")

    with (
        patch(
            "main.find_json_files", return_value=mock_json_files
        ) as mock_find_json_files,
        patch(
            "main.get_morphemes_from_songs", return_value=pd.DataFrame()
        ) as mock_get_morphemes,
    ):
        response = client.post("/extract-morphemes/")
        assert response.status_code == 404
        assert response.json()["detail"] == "No morphemes found in the JSON files."
        mock_find_json_files.assert_called_once_with("test_dir")
        mock_get_morphemes.assert_called_once_with(mock_json_files)


def test_extract_morphemes_missing_json_dir(monkeypatch):
    monkeypatch.delenv("JSON_DIR", raising=False)
    monkeypatch.setenv("DB_USER", "test")
    monkeypatch.setenv("DB_PASSWORD", "test")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")
    with patch("main.find_json_files") as mock_find_json_files:
        response = client.post("/extract-morphemes/")
        assert response.status_code == 400
        assert (
            response.json()["detail"] == "JSON_DIR enviroment viable must be provided."
        )
        mock_find_json_files.assert_not_called()


def test_visualize_success(monkeypatch, mock_dataframe):
    monkeypatch.setenv("DB_USER", "test")
    monkeypatch.setenv("DB_PASSWORD", "test")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")
    with (
        patch(
            "main.load_morpheme_table", return_value=mock_dataframe
        ) as mock_load_morpheme_table,
        patch("main.plot_top_morphemes") as mock_plot_top_morphemes,
        patch("main.plot_pos_distribution") as mock_plot_pos_distribution,
        patch("main.plot_morpheme_song_heatmap") as mock_plot_heatmap,
        patch(
            "main.setup_visualization", return_value={"title": 10}
        ) as mock_setup_visualization,
    ):
        response = client.post("/visualize/", params={"font_scale": 2.0})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Plots saved successfully."
        assert "visual_output/top_morphemes.png" in data["output_files"]
        mock_load_morpheme_table.assert_called()
        mock_plot_top_morphemes.assert_called()
        mock_plot_pos_distribution.assert_called()
        mock_plot_heatmap.assert_called()
        mock_setup_visualization.assert_called_with(2.0)
