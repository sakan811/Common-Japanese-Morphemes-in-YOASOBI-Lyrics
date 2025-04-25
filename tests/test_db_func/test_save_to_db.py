from unittest.mock import patch

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from morphemes_extractor.db_func import save_to_db


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Morpheme": ["テスト", "データ"],
            "Romanji": ["tesuto", "de-ta"],
            "Part_of_Speech": ["Noun", "Noun"],
            "Song": ["Test Song", "Test Song"],
            "Song_Romanji": ["Tesuto Songu", "Tesuto Songu"],
        }
    )


def test_successful_save(tmp_path, sample_df):
    db_path = tmp_path / "test.db"
    db_url = f"sqlite:///{db_path}"
    save_to_db(sample_df, db_url)

    # Verify the data was saved correctly
    engine = create_engine(db_url)
    with engine.connect() as conn:
        saved_df = pd.read_sql_table("Morpheme", conn)

    pd.testing.assert_frame_equal(sample_df, saved_df)


def test_overwrite_existing_table(tmp_path, sample_df):
    db_path = tmp_path / "test.db"
    db_url = f"sqlite:///{db_path}"

    # Save initial data
    save_to_db(sample_df, db_url)

    # Create new data and overwrite
    new_df = pd.DataFrame(
        {
            "Morpheme": ["新しい"],
            "Romanji": ["atarashii"],
            "Part_of_Speech": ["Adjective"],
            "Song": ["New Song"],
            "Song_Romanji": ["Nyu- Songu"],
        }
    )
    save_to_db(new_df, db_url)

    # Verify the new data overwrote the old data
    engine = create_engine(db_url)
    with engine.connect() as conn:
        saved_df = pd.read_sql_table("Morpheme", conn)

    pd.testing.assert_frame_equal(new_df, saved_df)


@patch("morphemes_extractor.db_func.create_engine")
def test_error_handling_operational_error(mock_create_engine, tmp_path, sample_df):
    db_path = tmp_path / "nonexistent_db.sqlite"
    invalid_url = f"sqlite:///{db_path}"

    # Configure the mock to raise an OperationalError
    mock_create_engine.side_effect = OperationalError("mocked error", None, None)

    with pytest.raises(OperationalError):
        save_to_db(sample_df, invalid_url)

    # Verify that create_engine was called with the correct URL
    mock_create_engine.assert_called_once_with(invalid_url)
