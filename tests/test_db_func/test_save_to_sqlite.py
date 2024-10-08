import pytest
import pandas as pd
import sqlite3
from morphemes_extractor.db_func import save_to_sqlite


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Morpheme': ['テスト', 'データ'],
        'Romanji': ['tesuto', 'de-ta'],
        'Part_of_Speech': ['Noun', 'Noun'],
        'Song': ['Test Song', 'Test Song'],
        'Song_Romanji': ['Tesuto Songu', 'Tesuto Songu']
    })


def test_successful_save(tmp_path, sample_df):
    db_path = tmp_path / "test.db"
    save_to_sqlite(sample_df, str(db_path))

    # Verify the data was saved correctly
    with sqlite3.connect(str(db_path)) as conn:
        saved_df = pd.read_sql_query("SELECT * FROM Morpheme", conn)

    pd.testing.assert_frame_equal(sample_df, saved_df)


def test_overwrite_existing_table(tmp_path, sample_df):
    db_path = tmp_path / "test.db"

    # Save initial data
    save_to_sqlite(sample_df, str(db_path))

    # Create new data and overwrite
    new_df = pd.DataFrame({
        'Morpheme': ['新しい'],
        'Romanji': ['atarashii'],
        'Part_of_Speech': ['Adjective'],
        'Song': ['New Song'],
        'Song_Romanji': ['Nyu- Songu']
    })
    save_to_sqlite(new_df, str(db_path))

    # Verify the new data overwrote the old data
    with sqlite3.connect(str(db_path)) as conn:
        saved_df = pd.read_sql_query("SELECT * FROM Morpheme", conn)

    pd.testing.assert_frame_equal(new_df, saved_df)


def test_error_handling(tmp_path, sample_df):
    invalid_path = "/invalid/path/test.db"
    with pytest.raises(sqlite3.OperationalError):
        save_to_sqlite(sample_df, invalid_path)

