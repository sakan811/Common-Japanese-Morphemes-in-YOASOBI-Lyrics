import asyncio
import sqlite3
import sys

from loguru import logger

from scraper.data_extractor import extract_data
from scraper.data_transformer import transform_data_to_df
from scraper.sql_query import create_morpheme_table_query, delete_all_rows
from scraper.web_scraper import return_url_list, async_fetch_page_sources, get_lyrics_list

logger.configure(handlers=[{'sink': sys.stdout, 'level': 'INFO'}])
logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w', level="INFO")


def start_scraper(db_dir: str) -> None:
    """
    Start a web-scraper that fetches YOASOBI's songs' lyrics from Genius.com
    :param db_dir: Database directory.
    :return: None
    """
    logger.info('Starting a web-scraper...')

    urls: list[str] = return_url_list()
    page_source_list: list[bytes] = asyncio.run(async_fetch_page_sources(urls))

    with sqlite3.connect(db_dir) as conn:
        query = create_morpheme_table_query()
        conn.execute(query)
        conn.commit()

    if page_source_list:
        logger.info(f'The \'page sources list\' is not empty.')

        logger.info(f'Delete all rows from the \'Morpheme\' table.')
        with sqlite3.connect(db_dir) as conn:
            query = delete_all_rows()
            conn.execute(query)
            conn.commit()

        lyrics_lists: list[list[str]] = get_lyrics_list(page_source_list)

        if lyrics_lists:
            for lyrics_list in lyrics_lists:
                morphemes, romanized_morphemes, part_of_speech_list, song_name = extract_data(lyrics_list)

                df = transform_data_to_df(morphemes, romanized_morphemes, part_of_speech_list, song_name)

                df.to_sql('Morpheme', conn, if_exists='append', index=False)
        else:
            logger.warning('No lyrics were found. Skipping this page source...')
    else:
        logger.warning('No page sources were found. Stop the process.')


if __name__ == '__main__':
    db_dir = 'yoasobi.db'
    start_scraper(db_dir)
