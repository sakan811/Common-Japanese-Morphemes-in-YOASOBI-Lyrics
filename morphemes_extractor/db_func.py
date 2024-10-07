import sqlite3

import pandas as pd
from loguru import logger


def execute_sqlite_query(db_dir: str, query: str) -> None:
    """
    Executes SQL query on database.
    :param db_dir: SQLite database directory.
    :param query: SQL query to execute.
    :return: None
    """
    logger.debug(f"Executing SQL query {query}")
    with sqlite3.connect(db_dir) as conn:
        conn.execute(query)
        conn.commit()


def save_to_sqlite(df: pd.DataFrame, db_dir: str) -> None:
    """
    Save a DataFrame to a SQLite database.

    :param df: DataFrame containing the morpheme data to be saved
    :param db_dir: Directory path of the SQLite database file
    :return: None

    This function connects to a SQLite database specified by db_dir and appends
    the data from the provided DataFrame to a table named 'Morpheme'. If the
    table doesn't exist, it will be created.

    The function uses a context manager to ensure proper connection handling.
    """
    with sqlite3.connect(db_dir) as conn:
        try:
            df.to_sql('Morpheme', conn, if_exists='replace', index=False)
        except sqlite3.OperationalError as e:
            logger.error(f"Error saving DataFrame to SQLite database: {e}")