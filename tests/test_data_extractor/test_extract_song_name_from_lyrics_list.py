import pytest

from morphemes_extractor.data_extractor import extract_song_name_from_lyrics_list


def test_extract_song_name_from_normal_case():
    lyrics_list = ["歌詞「歌の名前」その他の情報"]
    assert extract_song_name_from_lyrics_list(lyrics_list) == "歌の名前"


def test_extract_song_name_with_additional_text():
    lyrics_list = ["何か前にある 歌詞「歌の名前」その他の情報"]
    with pytest.raises(IndexError):
        extract_song_name_from_lyrics_list(lyrics_list)


def test_extract_song_name_with_multiple_quotations():
    lyrics_list = ["歌詞「歌の名前」その他「無視する」情報"]
    assert extract_song_name_from_lyrics_list(lyrics_list) == "歌の名前"


def test_extract_song_name_with_no_song_name():
    lyrics_list = ["歌詞「」その他の情報"]
    assert extract_song_name_from_lyrics_list(lyrics_list) == ""


def test_extract_song_name_with_no_quotation_marks():
    lyrics_list = ["歌詞その他の情報"]
    with pytest.raises(IndexError):
        extract_song_name_from_lyrics_list(lyrics_list)


def test_extract_song_name_from_empty_list():
    lyrics_list = [""]
    with pytest.raises(IndexError):
        extract_song_name_from_lyrics_list(lyrics_list)


def test_extract_song_name_with_space_in_song_name():
    lyrics_list = ["歌詞「歌 の 名前」その他の情報"]
    assert extract_song_name_from_lyrics_list(lyrics_list) == "歌"
