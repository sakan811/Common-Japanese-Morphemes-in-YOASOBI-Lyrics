from morphemes_extractor.data_extractor import extract_romanji


def test_extract_romanji_hiragana():
    assert extract_romanji("こんにちは") == "Konnichiha"


def test_extract_romanji_katakana():
    assert extract_romanji("コンピューター") == "Computer"


def test_extract_romanji_kanji():
    assert extract_romanji("日本語") == "Nippon go"


def test_extract_romanji_mixed():
    assert extract_romanji("私はAIです") == "Watakushi wa AI desu"


def test_extract_romanji_empty_string():
    assert extract_romanji("") == ""


def test_extract_romanji_non_japanese():
    assert extract_romanji("Hello") == "Hello"


def test_extract_romanji_special_characters():
    assert extract_romanji("ーッ！？") == "- !?"
