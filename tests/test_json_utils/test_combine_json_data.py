from morphemes_extractor.json_utils import combine_json_data


def test_combine_json_data_empty_list():
    result = combine_json_data([])
    assert result == {"songs": []}


def test_combine_json_data_single_dict():
    input_data = [{"songs": [{"title": "Song1", "artist": "Artist1"}]}]
    expected = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    assert combine_json_data(input_data) == expected


def test_combine_json_data_multiple_dicts():
    input_data = [
        {"songs": [{"title": "Song1", "artist": "Artist1"}]},
        {"songs": [{"title": "Song2", "artist": "Artist2"}]}
    ]
    expected = {
        "songs": [
            {"title": "Song1", "artist": "Artist1"},
            {"title": "Song2", "artist": "Artist2"}
        ]
    }
    assert combine_json_data(input_data) == expected


def test_combine_json_data_missing_songs_key():
    input_data = [
        {"songs": [{"title": "Song1", "artist": "Artist1"}]},
        {"not_songs": [{"title": "Song2", "artist": "Artist2"}]}
    ]
    expected = {"songs": [{"title": "Song1", "artist": "Artist1"}]}
    assert combine_json_data(input_data) == expected


def test_combine_json_data_mixed_content():
    input_data = [
        {"songs": [{"title": "Song1", "artist": "Artist1"}]},
        {"songs": []},
        {"songs": [{"title": "Song2", "artist": "Artist2"}, {"title": "Song3", "artist": "Artist3"}]}
    ]
    expected = {
        "songs": [
            {"title": "Song1", "artist": "Artist1"},
            {"title": "Song2", "artist": "Artist2"},
            {"title": "Song3", "artist": "Artist3"}
        ]
    }
    assert combine_json_data(input_data) == expected


def test_combine_json_data_return_type():
    result = combine_json_data([{"songs": []}])
    assert isinstance(result, dict)
    assert isinstance(result.get("songs"), list)
