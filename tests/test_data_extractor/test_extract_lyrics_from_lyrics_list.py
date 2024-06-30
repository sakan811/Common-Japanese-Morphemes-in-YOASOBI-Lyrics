from yoasobi_pipeline.yoasobi_scraper.data_extractor import extract_lyrics_from_lyrics_list


def test_extract_lyrics_normal_case():
    lyrics_list = ["[YOASOBI「心音」歌詞]\nFirst line of lyrics", "Second line of lyrics"]
    expected = "FirstlineoflyricsSecondlineoflyrics"
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected


def test_extract_lyrics_with_brackets():
    lyrics_list = ["[YOASOBI「心音」歌詞]\nFirst line of lyrics [extra]", "Second line of lyrics"]
    expected = "FirstlineoflyricsSecondlineoflyrics"
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected


def test_extract_lyrics_with_multiple_brackets():
    lyrics_list = ["[YOASOBI「心音」歌詞]\nFirst line of lyrics [extra]", "Second line of lyrics [extra]"]
    expected = "FirstlineoflyricsSecondlineoflyrics"
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected


def test_extract_lyrics_with_empty_list():
    lyrics_list = []
    expected = ""
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected


def test_extract_lyrics_with_only_song_name():
    lyrics_list = ["[YOASOBI「心音」歌詞]\n"]
    expected = ""
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected


def test_extract_lyrics_with_song_name_with_space():
    lyrics_list = ["[YOASOBI「心 音」歌詞]\nFirst line of lyrics"]
    expected = "音」歌詞]Firstlineoflyrics"
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected


def test_extract_lyrics_with_whitespace():
    lyrics_list = ["[YOASOBI「心音」歌詞]\nFirst line of lyrics", "  Second line of lyrics  ",
                   "  Third line of lyrics  "]
    expected = "FirstlineoflyricsSecondlineoflyricsThirdlineoflyrics"
    assert extract_lyrics_from_lyrics_list(lyrics_list) == expected
