import pytest
from morphemes_extractor.data_extractor import get_song_list


def test_get_song_list_valid_input():
    json_data = {
        "songs": [
            {"title": "Song 1", "romanji_title": "Song One", "lyrics": "Lyrics 1"},
            {"title": "Song 2", "romanji_title": "Song Two", "lyrics": "Lyrics 2"},
        ]
    }

    result = get_song_list(json_data)

    assert len(result) == 2
    assert result[0]["title"] == "Song 1"
    assert result[1]["romanji_title"] == "Song Two"


def test_get_song_list_empty_list():
    json_data = {"songs": []}

    result = get_song_list(json_data)

    assert result == []


def test_get_song_list_missing_key():
    json_data = {"not_songs": []}

    with pytest.raises(KeyError) as exc_info:
        get_song_list(json_data)

    assert str(exc_info.value) == "'songs'"
