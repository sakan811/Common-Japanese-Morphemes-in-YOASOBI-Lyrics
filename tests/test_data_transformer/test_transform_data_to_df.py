import pytest

from morphemes_extractor.data_transformer import transform_data_to_df


def test_transform_data_with_morpheme_true(mocker):
    # Given
    char_list = ['サクラ', 'サクラ', 'サクラ']
    romanized_char_list = ['sakura', 'sakura', 'sakura']
    part_of_speech_list = ['noun', 'verb', 'adjective']
    song_name = 'さくら'
    is_morpheme = True

    mocker.patch('scraper.data_transformer.extract_romanji', return_value='sakura')

    # When
    df = transform_data_to_df(char_list, romanized_char_list, part_of_speech_list, song_name, is_morpheme)

    # Then
    assert not df.empty
    assert list(df.columns) == ['Morpheme', 'Romanji', 'Part_of_Speech', 'Song', 'Song_Romanji', 'Timestamp']
    assert df['Morpheme'].tolist() == char_list
    assert df['Romanji'].tolist() == romanized_char_list
    assert df['Part_of_Speech'].tolist() == part_of_speech_list
    assert df['Song'].iloc[0] == song_name
    assert df['Song_Romanji'].iloc[0] == 'sakura'


def test_transform_data_with_empty_lists(mocker):
    # Given
    char_list = []
    romanized_char_list = []
    part_of_speech_list = []
    song_name = 'さくら'
    is_morpheme = False

    mocker.patch('scraper.data_transformer.extract_romanji', return_value='sakura')

    # When
    df = transform_data_to_df(char_list, romanized_char_list, part_of_speech_list, song_name, is_morpheme)

    # Then
    assert df.empty
    assert list(df.columns) == ['Word', 'Romanji', 'Part_of_Speech', 'Song', 'Song_Romanji', 'Timestamp']


def test_transform_data_to_df_with_morpheme_flag_false(mocker):
    # Given
    char_list = ['日', '本', '語']
    romanized_char_list = ['ni', 'hon', 'go']
    part_of_speech_list = ['Noun', 'Noun', 'Noun']
    song_name = 'ありがとう'
    is_morpheme = False

    expected_columns = ['Word', 'Romanji', 'Part_of_Speech', 'Song', 'Song_Romanji', 'Timestamp']

    # Mocking the extract_romanji function
    mocker.patch('scraper.data_transformer.extract_romanji', return_value='arigatou')

    # When
    result_df = transform_data_to_df(char_list, romanized_char_list, part_of_speech_list, song_name, is_morpheme)

    # Then
    assert result_df.columns.tolist() == expected_columns
    assert result_df['Word'].tolist() == char_list
    assert result_df['Romanji'].tolist() == romanized_char_list
    assert result_df['Part_of_Speech'].tolist() == part_of_speech_list
    assert result_df['Song'].tolist() == [song_name] * len(char_list)
    assert result_df['Song_Romanji'].tolist() == ['arigatou'] * len(char_list)
    assert result_df['Timestamp'].notnull().all()


def test_mismatched_lengths_input_lists():
    # Given
    char_list = ['日', '本', '語']
    romanized_char_list = ['ni', 'hon']
    part_of_speech_list = ['Noun', 'Noun', 'Noun']
    song_name = 'ありがとう'
    is_morpheme = True

    # When
    with pytest.raises(ValueError):
        transform_data_to_df(char_list, romanized_char_list, part_of_speech_list, song_name, is_morpheme)

    # Then
    # Expecting a ValueError due to mismatched lengths of input lists
