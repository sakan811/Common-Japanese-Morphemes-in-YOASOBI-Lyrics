from datetime import datetime
from typing import Any
from sqlalchemy import create_engine, Engine, text, Sequence
from sqlalchemy.cyextension.util import Mapping
from loguru import logger

from yoasobi_project_package import extract as ext
from yoasobi_project_package import sql_query as sqlquery


def connect_sqlite_db(db_dir: str) -> Engine:
    """
    Create the SQLite database if not exists.
    Connect to the SQLite database.
    :param db_dir: Database directory String
    :return: sqlalchemy Engine object
    """
    logger.info('Creating Engine...')
    engine: Engine = create_engine(f'sqlite:///{db_dir}', echo=True)
    return engine


def execute_sql_query(
        engine: Engine,
        sql_query: str,
        params: Sequence[Mapping[str, Any]] | Mapping[str, Any] | None = None) -> None:
    """
    Execute the given SQL query.
    :param engine: sqlalchemy Engine Object
    :param sql_query: SQL query String
    :param params: Dictionary[String, String] or None. None is default.
    :return: None
    """
    logger.info(f'Execute {sql_query = }...')
    try:
        logger.info('Get a connection to the database')
        with engine.connect() as connection:
            logger.info('Execute SQL query')
            connection.execute(text(sql_query), params)

            logger.info('Commit database')
            connection.commit()
    except Exception as e:
        logger.error(f'Error: {e}')

        logger.info('Rollback database')
        connection.rollback()


def table_exists(table_name: str, db_dir: str) -> bool:
    """
    Check whether the table exists.
    :param db_dir: Database directory String
    :param table_name: Table's name
    :return: Boolean
    """
    logger.info('Get a connection to the database')
    engine = connect_sqlite_db(db_dir)
    with engine.connect() as con:
        logger.info(f'Query to check if the {table_name = } exists')

        query_text = "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
        logger.debug(f'{query_text = }')
        query = text(query_text)

        params = {"table_name": table_name}
        logger.debug(f'{params = }')

        logger.info('Execute the query with parameters')
        result = con.execute(query, params).fetchone()
        logger.debug(f'{result = }')

    # Return True if the table exists, False otherwise
    return result is not None


def insert_data(
        words: list[str],
        romanized_words: list[str],
        part_of_speech_list: list[str],
        song_name: str,
        db_dir: str) -> None:
    """
    Insert data into the table. If the table does not exist, return.
    :param db_dir: Database directory String
    :param part_of_speech_list: List of Japanese Part of Speech String.
                                Exclude English words and Japanese Auxiliary Symbols.
    :param words: List of Japanese words String
    :param romanized_words: List of Romanjis String
    :param song_name: Song name String
    :return: None
    """
    logger.info('Insert data into table...')
    song_name_romanji: str = ext.extract_romanji(song_name)
    logger.debug(f'{song_name_romanji = }')

    engine: Engine = connect_sqlite_db(db_dir)

    sql_query = sqlquery.insert_data_query()
    logger.info(f'{sql_query = }')

    timestamp = datetime.now()
    logger.debug(f'{timestamp = }')

    table_name = 'Words'
    logger.debug(f'{table_name = }')

    if table_exists(table_name, db_dir):
        logger.info('Zip \'words\', \'romanized_words\', \'part_of_speech_list\' together'
                    'and loop through them')
        for word, romanized_word, part_of_speech in zip(words, romanized_words, part_of_speech_list):
            data = {
                'Kanji': word,
                'Romanji': romanized_word,
                'Part_of_Speech': part_of_speech,
                'Song': song_name,
                'Song_Romanji': song_name_romanji,
                'Timestamp': timestamp
            }
            logger.debug(f'{data = }')

            execute_sql_query(engine, sql_query, data)
    else:
        logger.info(f'Table \'{table_name}\' does not exist.')
        return


if __name__ == '__main__':
    pass
