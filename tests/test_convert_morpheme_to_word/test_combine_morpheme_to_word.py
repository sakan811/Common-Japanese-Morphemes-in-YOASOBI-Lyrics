from convert_morpheme_to_word import combine_morpheme_to_word


def test_combine_morpheme_to_word_success():
    # Given
    morphemes = ['日', '本', '語', '英', '語']
    dictionary = {'日本語': True, '英語': True, '日本': True}
    max_word_length = 5

    # When
    result = combine_morpheme_to_word(morphemes, dictionary, max_word_length)

    # Then
    assert result == ['日本語', '英語']  # '日本語' and '英語' are valid combinations


def test_combine_morpheme_to_word_no_valid_combination():
    # Given
    morphemes = ['a', 'b', 'c']
    dictionary = {'abc': True}
    max_word_length = 3

    # When
    result = combine_morpheme_to_word(morphemes, dictionary, max_word_length)

    # Then
    assert result == ['abc']


def test_combine_morpheme_to_word_empty_morphemes():
    # Given
    morphemes = []
    dictionary = {'日本語': True, '英語': True}
    max_word_length = 5

    # When
    result = combine_morpheme_to_word(morphemes, dictionary, max_word_length)

    # Then
    assert result == []  # No morphemes to combine


def test_combine_morpheme_to_word_empty_dictionary():
    # Given
    morphemes = ['日', '本', '語']
    dictionary = {}  # Empty dictionary
    max_word_length = 5

    # When
    result = combine_morpheme_to_word(morphemes, dictionary, max_word_length)

    # Then
    assert result == []  # No valid words in the dictionary


def test_combine_morpheme_to_word_max_word_length():
    # Given
    morphemes = ['日', '本', '語', '英', '語']
    dictionary = {'日本語': True, '日本': True, '英語': True}
    max_word_length = 2

    # When
    result = combine_morpheme_to_word(morphemes, dictionary, max_word_length)

    # Then
    assert result == ['日本', '英語']
