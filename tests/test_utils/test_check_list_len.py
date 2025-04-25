from morphemes_extractor.utils import check_list_len
from morphemes_extractor.jp_data import MorphemeData


def test_check_list_len_single_list():
    morpheme_data = MorphemeData(
        morphemes=["word1", "word2", "word3"],
        romanized_morphemes=["word1", "word2", "word3"],
        part_of_speech_list=["noun", "verb", "adj"],
    )
    assert check_list_len(morpheme_data) == (3, 3, 3)


def test_check_list_len_empty_list():
    morpheme_data = MorphemeData(
        morphemes=[], romanized_morphemes=[], part_of_speech_list=[]
    )
    assert check_list_len(morpheme_data) == (0, 0, 0)


def test_check_list_len_mixed_length_lists():
    morpheme_data = MorphemeData(
        morphemes=["word1", "word2", "word3"],
        romanized_morphemes=["word1", "word2"],
        part_of_speech_list=["noun", "verb", "adj", "adv"],
    )
    assert check_list_len(morpheme_data) == (3, 2, 4)


def test_check_list_len_single_item_lists():
    morpheme_data = MorphemeData(
        morphemes=["word1"],
        romanized_morphemes=["romanized1"],
        part_of_speech_list=["noun"],
    )
    assert check_list_len(morpheme_data) == (1, 1, 1)


def test_check_list_len_with_different_data_types():
    morpheme_data = MorphemeData(
        morphemes=["word1", "word2"],
        romanized_morphemes=["a", "b", "c"],
        part_of_speech_list=["noun", "verb", "adj"],
    )
    assert check_list_len(morpheme_data) == (2, 3, 3)
