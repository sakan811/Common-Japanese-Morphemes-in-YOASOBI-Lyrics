import sqlite3
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
