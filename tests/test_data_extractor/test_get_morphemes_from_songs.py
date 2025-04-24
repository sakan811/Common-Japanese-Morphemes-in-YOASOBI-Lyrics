import pytest
import pandas as pd
from unittest.mock import patch
from morphemes_extractor.data_extractor import get_morphemes_from_songs


@pytest.fixture
def mock_dependencies():
    with (
        patch("morphemes_extractor.data_extractor.load_json") as mock_load_json,
        patch("morphemes_extractor.data_extractor.get_song_list") as mock_get_song_list,
        patch("morphemes_extractor.data_extractor.extract_data") as mock_extract_data,
        patch(
            "morphemes_extractor.data_extractor.transform_data_to_df"
        ) as mock_transform_data_to_df,
    ):
        yield (
            mock_load_json,
            mock_get_song_list,
            mock_extract_data,
            mock_transform_data_to_df,
        )


def test_get_morphemes_from_songs_valid_data(mock_dependencies):
    mock_load_json, mock_get_song_list, mock_extract_data, mock_transform_data_to_df = (
        mock_dependencies
    )

    mock_load_json.return_value = {"songs": [{"title": "Song 1"}]}
    mock_get_song_list.return_value = [{"title": "Song 1"}]
    mock_extract_data.return_value = (
        ["word1"],
        ["romanized1"],
        ["pos1"],
        "Song 1",
        "Song One",
    )
    mock_transform_data_to_df.return_value = pd.DataFrame(
        {"morphemes": ["word1"], "romanized": ["romanized1"], "pos": ["pos1"]}
    )

    result = get_morphemes_from_songs(["path/to/json"])

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == ["morphemes", "romanized", "pos"]
    assert result["morphemes"].tolist() == ["word1"]


def test_get_morphemes_from_songs_empty_data(mock_dependencies):
    mock_load_json, mock_get_song_list, mock_extract_data, mock_transform_data_to_df = (
        mock_dependencies
    )

    mock_load_json.return_value = {"songs": []}
    mock_get_song_list.return_value = []

    result = get_morphemes_from_songs(["path/to/json"])

    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_get_morphemes_from_songs_invalid_data(mock_dependencies):
    mock_load_json, mock_get_song_list, mock_extract_data, mock_transform_data_to_df = (
        mock_dependencies
    )

    mock_load_json.return_value = {"songs": [{"title": "Song 1"}]}
    mock_get_song_list.return_value = [{"title": "Song 1"}]
    mock_extract_data.return_value = (
        ["word1"],
        ["romanized1"],
        ["pos1"],
        "Song 1",
        "Song One",
    )
    mock_transform_data_to_df.return_value = pd.DataFrame()  # Empty DataFrame

    result = get_morphemes_from_songs(["path/to/json"])

    assert isinstance(result, pd.DataFrame)
    assert result.empty
