from sqlalchemy import Engine
from loguru import logger

from yoasobi_project import extract as ext
from yoasobi_project import sqlite_db as sqldb
from yoasobi_project import utils as ut
from yoasobi_project import web_scrap as ws

# Prevent Loguru to show log message in terminal.
logger.remove()

logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def main() -> None:
    try:
        db_dir = 'yoasobi.db'
        logger.debug(f'{db_dir = }')

        sqlite_db: Engine = sqldb.connect_sqlite_db(db_dir)
        logger.debug(f'{sqlite_db = }')

        logger.info('Checking if \'sql_query_exist\' exists')

        while True:
            option_result: str | None = ut.choose_table_options()
            logger.debug(f'{option_result = }')

            sql_query_exist: bool | None = ut.check_table_sql_query(option_result, sqlite_db)
            logger.debug(f'{sql_query_exist = }')

            if sql_query_exist:
                logger.info(f'{sql_query_exist = }. Continue...')
                continue
            else:
                logger.info(f'{sql_query_exist = }. Break the loop...')
                break

        urls: list[str] = ws.return_url_list()
        for url in urls:
            lyrics_list: list[str] = ws.scrap(url)
            logger.debug(f'{lyrics_list = }')

            song_name: str = ws.extract_song_name_from_lyrics_list(lyrics_list)
            logger.debug(f'{song_name = }')

            lyrics: str = ws.extract_lyrics_from_lyrics_list(lyrics_list)
            logger.debug(f'{lyrics = }')

            words: list[str] = ext.extract_words_from_lyrics(lyrics)
            logger.debug(f'{words = }')

            romanized_words: list[str] = ext.extract_romanji_from_words(words)
            logger.debug(f'{romanized_words = }')

            part_of_speech_list: list[str] = ext.extract_part_of_speech_from_words(words)
            logger.debug(f'{part_of_speech_list = }')

            sqldb.insert_data(words, romanized_words, part_of_speech_list, song_name, db_dir)

            print(f'{len(words) = }')
            print(f'{len(romanized_words) = }')
            print(f'{len(part_of_speech_list) = }')
    except Exception as e:
        logger.error(f'Error: {e}')


if __name__ == '__main__':
    main()
