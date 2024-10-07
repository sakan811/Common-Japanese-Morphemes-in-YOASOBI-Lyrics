from morphemes_extractor.data_extractor import is_english


def test_is_english_with_english_word():
    assert is_english("hello") is True


def test_is_english_with_mixed_characters():
    assert is_english("hello123") is True


def test_is_english_with_non_english_characters():
    assert is_english("こんにちは") is False


def test_is_english_with_empty_string():
    assert is_english("") is False


def test_is_english_with_numbers_only():
    assert is_english("123456") is False


def test_is_english_with_special_characters():
    assert is_english("@#$%^&*") is False


def test_is_english_with_english_and_non_english_characters():
    assert is_english("helloこんにちは") is True


def test_is_english_with_space():
    assert is_english("hello world") is True


def test_is_english_with_punctuation():
    assert is_english("hello!") is True
