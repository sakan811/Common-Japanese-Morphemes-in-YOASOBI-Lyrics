from scraper.data_extractor import extract_part_of_speech_from_morphemes


def test_extract_pos_with_japanese_words():
    words = ["こんにちは", "世界", "食べる", "美しい"]
    assert extract_part_of_speech_from_morphemes(words) == ['Interjection', 'Noun', 'Verb', 'Adjective']


def test_extract_pos_with_english_words():
    words = ["hello", "world"]
    assert extract_part_of_speech_from_morphemes(words) == ['Noun', 'Noun']


def test_extract_pos_with_mixed_words():
    words = ["こんにちは", "world", "食べる"]
    assert extract_part_of_speech_from_morphemes(words) == ['Interjection', 'Noun', 'Verb']


def test_extract_pos_with_auxiliary_symbols():
    words = ["こんにちは", "です"]
    assert extract_part_of_speech_from_morphemes(words) == ['Interjection', 'Auxiliary Verb']


def test_extract_pos_with_empty_list():
    words = []
    assert extract_part_of_speech_from_morphemes(words) == []


def test_extract_pos_with_special_characters():
    words = ["こんにちは!", "食べる?"]
    assert extract_part_of_speech_from_morphemes(words) == ['Interjection', 'Verb']
