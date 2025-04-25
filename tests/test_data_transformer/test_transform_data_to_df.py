import pytest
import pandas as pd
from datetime import datetime

from morphemes_extractor.data_transformer import transform_data_to_df


@pytest.fixture
def sample_data():
    return {
        "char_list": ["私", "は", "歌う"],
        "romanized_char_list": ["watashi", "wa", "utau"],
        "part_of_speech_list": ["pronoun", "particle", "verb"],
        "song_name": "素敵な歌",
        "song_romanized_name": "Suteki na Uta",
    }


def test_return_type(sample_data):
    df = transform_data_to_df(**sample_data)
    assert isinstance(df, pd.DataFrame)


def test_dataframe_shape(sample_data):
    df = transform_data_to_df(**sample_data)
    assert df.shape == (3, 6)  # 3 rows, 6 columns


def test_column_names(sample_data):
    df = transform_data_to_df(**sample_data)
    expected_columns = [
        "Morpheme",
        "Romanji",
        "Part_of_Speech",
        "Song",
        "Song_Romanji",
        "Timestamp",
    ]
    assert list(df.columns) == expected_columns


def test_data_integrity(sample_data):
    df = transform_data_to_df(**sample_data)
    assert df["Morpheme"].tolist() == sample_data["char_list"]
    assert df["Romanji"].tolist() == sample_data["romanized_char_list"]
    assert df["Part_of_Speech"].tolist() == sample_data["part_of_speech_list"]
    assert df["Song"].iloc[0] == sample_data["song_name"]
    assert df["Song_Romanji"].iloc[0] == sample_data["song_romanized_name"]


def test_timestamp_format(sample_data):
    df = transform_data_to_df(**sample_data)
    timestamp = datetime.strptime(df["Timestamp"].iloc[0], "%Y-%m-%d %H:%M:%S")
    assert isinstance(timestamp, datetime)


def test_empty_input():
    empty_df = transform_data_to_df([], [], [], "空の歌", "Empty Song")
    assert empty_df.shape == (0, 6)


if __name__ == "__main__":
    pytest.main()
