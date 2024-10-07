from unittest.mock import patch

import pytest
from morphemes_extractor.data_extractor import extract_data


def test_extract_data_valid_input():
    song = {
        'title': 'テスト曲',
        'romanji_title': 'Test Song',
        'lyrics': 'こんにちは 世界'
    }

    morphemes, romanized, pos, name, eng_name = extract_data(song)

    assert morphemes == ['こんにちは', '世界']
    assert romanized == ['Konnichiha', 'Sekai']
    assert pos == ['Interjection', 'Noun']
    assert name == 'テスト曲'
    assert eng_name == 'Test Song'


def test_extract_data_empty_lyrics():
    song = {
        'title': 'Empty Song',
        'romanji_title': 'Empty Song',
        'lyrics': ''
    }

    morphemes, romanized, pos, name, eng_name = extract_data(song)

    assert morphemes == []
    assert romanized == []
    assert pos == []
    assert name == 'Empty Song'
    assert eng_name == 'Empty Song'


def test_extract_data_unequal_list_lengths():
    song = {
        'title': 'Unequal Song',
        'romanji_title': 'Unequal Song',
        'lyrics': 'テスト'
    }

    # Mock the extract functions to return lists of different lengths
    with patch('morphemes_extractor.data_extractor.extract_morphemes_from_lyrics', return_value=['テスト']), \
            patch('morphemes_extractor.data_extractor.extract_romanji_from_jp_characters',
                  return_value=['Test', 'Extra']), \
            patch('morphemes_extractor.data_extractor.extract_part_of_speech_from_morphemes', return_value=['Noun']):
        with pytest.raises(Exception) as exc_info:
            extract_data(song)

        assert str(exc_info.value) == 'The length of words, romanized_morphemes, and part_of_speech_list are not equal.'