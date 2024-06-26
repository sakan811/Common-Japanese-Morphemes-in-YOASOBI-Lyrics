from yoasobi_pipeline.yoasobi_scraper.data_extractor import extract_romanji_from_words


def test_extract_romanji_from_japanese_words():
    words = ["こんにちは", "世界", "食べる", "美しい"]
    assert extract_romanji_from_words(words) == ['Konnichiha', 'Sekai', 'Taberu', 'Utsukushii']


def test_extract_romanji_from_mixed_words():
    words = ["こんにちは", "hello", "食べる", "world"]
    assert extract_romanji_from_words(words) == ['Konnichiha', 'Hello', 'Taberu', 'World']


def test_extract_romanji_with_english_words():
    words = ["hello", "world"]
    assert extract_romanji_from_words(words) == ['Hello', 'World']


def test_extract_romanji_with_empty_list():
    words = []
    assert extract_romanji_from_words(words) == []


def test_extract_romanji_with_special_characters():
    words = ["こんにちは!", "食べる?"]
    assert extract_romanji_from_words(words) == ['Konnichiha!', 'Taberu?']



