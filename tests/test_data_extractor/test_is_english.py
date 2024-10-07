from morphemes_extractor.data_extractor import is_english


def test_is_english_with_english_word():
    assert is_english("hello") == True


def test_is_english_with_mixed_characters():
    assert is_english("hello123") == True


def test_is_english_with_non_english_characters():
    assert is_english("こんにちは") == False


def test_is_english_with_empty_string():
    assert is_english("") == False


def test_is_english_with_numbers_only():
    assert is_english("123456") == False


def test_is_english_with_special_characters():
    assert is_english("@#$%^&*") == False


def test_is_english_with_english_and_non_english_characters():
    assert is_english("helloこんにちは") == True


def test_is_english_with_space():
    assert is_english("hello world") == True


def test_is_english_with_punctuation():
    assert is_english("hello!") == True
