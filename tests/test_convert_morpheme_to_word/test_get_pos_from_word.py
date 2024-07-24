from convert_morpheme_to_word import get_pos_from_word


def test_get_pos_from_word_success():
    # Given
    word_list = ['猫', '犬', '走る']
    jp_dict = {
        '猫': [{'part_of_speech': '名詞'}],
        '犬': [{'part_of_speech': '名詞'}],
        '走る': [{'part_of_speech': '動詞'}]
    }

    # When
    result = get_pos_from_word(word_list, jp_dict)

    # Then
    assert result == ['名詞', '名詞', '動詞']  # Expected parts of speech


def test_get_pos_from_word_empty_list():
    # Given
    word_list = []
    jp_dict = {
        '猫': [{'part_of_speech': '名詞'}],
        '犬': [{'part_of_speech': '名詞'}],
        '走る': [{'part_of_speech': '動詞'}]
    }

    # When
    result = get_pos_from_word(word_list, jp_dict)

    # Then
    assert result == []  # No words to process


def test_get_pos_from_word_word_not_in_dict():
    # Given
    word_list = ['猫', '鳥', '走る']
    jp_dict = {
        '猫': [{'part_of_speech': '名詞'}],
        '走る': [{'part_of_speech': '動詞'}]
    }

    # When
    result = get_pos_from_word(word_list, jp_dict)

    # Then
    assert result == ['名詞', None, '動詞']  # '鳥' not in dict should be handled


def test_get_pos_from_word_all_words_not_in_dict():
    # Given
    word_list = ['鳥', '魚', '花']
    jp_dict = {}

    # When
    result = get_pos_from_word(word_list, jp_dict)

    # Then
    assert result == [None, None, None]  # All words not in dict should be handled


def test_get_pos_from_word_partial_dict():
    # Given
    word_list = ['猫', '走る', '人']
    jp_dict = {
        '猫': [{'part_of_speech': '名詞'}],
        '走る': [{'part_of_speech': '動詞'}]
        # '人' is missing
    }

    # When
    result = get_pos_from_word(word_list, jp_dict)

    # Then
    assert result == ['名詞', '動詞', None]  # '人' not in dict should be handled


