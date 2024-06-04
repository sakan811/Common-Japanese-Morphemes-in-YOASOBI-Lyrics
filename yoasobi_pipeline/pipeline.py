from loguru import logger

from yoasobi_pipeline.yoasobi_scraper.data_extractor import extract_data
from yoasobi_pipeline.yoasobi_scraper.sql_query import create_table_query, delete_all_rows
from yoasobi_pipeline.yoasobi_scraper.sqlite_db import execute_sql_query, connect_sqlite_db, insert_data
from yoasobi_pipeline.yoasobi_scraper.web_scraper import return_url_list, thread_fetch_page_source, scrape


def get_all_page_source() -> list[bytes]:
    """
    Get all page sources from the URL list.
    :return: Page source list.
    """
    logger.info('Get all page sources...')
    urls: list[str] = return_url_list()
    page_source_list = thread_fetch_page_source(urls)
    return page_source_list


def create_table_if_not_exist(db_dir) -> None:
    """
    Create 'Words' table if not exists.
    :param db_dir: Database directory.
    :return: None
    """
    logger.info("Create 'Words' table if not exists...")
    engine = connect_sqlite_db(db_dir)
    query = create_table_query()
    execute_sql_query(engine, query)


def delete_all_row(db_dir) -> None:
    """
    Delete all rows from the 'Words' table.
    :param db_dir: Database directory.
    :return: None
    """
    logger.info("Delete all rows from the 'Words' table...")
    engine = connect_sqlite_db(db_dir)
    query = delete_all_rows()
    execute_sql_query(engine, query)


def scrape_each_page_source(db_dir, page_source_list) -> None:
    """
    Scrape each page source.
    :param db_dir: Database directory.
    :param page_source_list: List of page sources.
    :return: Tuple of scraped data.
    """
    logger.info('Scraping each page source...')
    for page_source in page_source_list:
        lyrics_list: list[str] = scrape(page_source)

        if lyrics_list:
            words, romanized_words, part_of_speech_list, song_name = extract_data(lyrics_list)

            insert_data(words, romanized_words, part_of_speech_list, song_name, db_dir)
        else:
            logger.warning('No lyrics were found. Skipping this page source...')


if __name__ == '__main__':
    pass
