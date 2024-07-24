from scraper.data_extractor import extract_words_from_lyrics


def test_extract_words_with_english_words():
    lyrics = "Hello world こんにちは"
    assert extract_words_from_lyrics(lyrics) == ["こんにちは"]


def test_extract_words_with_numbers():
    lyrics = "123 こんにちは"
    assert extract_words_from_lyrics(lyrics) == ["こんにちは"]


def test_extract_words_with_japanese_auxiliary_symbols():
    lyrics = "こんにちは です"
    assert extract_words_from_lyrics(lyrics) == ['こんにちは', 'です']


def test_extract_words_with_mixed_characters():
    lyrics = "Hello 123 こんにちは 世界"
    assert extract_words_from_lyrics(lyrics) == ["こんにちは", "世界"]


def test_extract_words_with_empty_string():
    lyrics = ""
    assert extract_words_from_lyrics(lyrics) == []


def test_extract_words_with_whitespace():
    lyrics = " こんにちは 世界 "
    assert extract_words_from_lyrics(lyrics) == ["こんにちは", "世界"]


def test_extract_words_with_newlines():
    lyrics = "こんにちは\n世界"
    assert extract_words_from_lyrics(lyrics) == ["こんにちは", "世界"]


def test_extract_words_with_special_characters():
    lyrics = "こんにちは! 世界?"
    assert extract_words_from_lyrics(lyrics) == ['こんにちは', '世界']
