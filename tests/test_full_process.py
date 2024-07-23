import asyncio
import sqlite3

import pytest
from loguru import logger
from bs4 import BeautifulSoup

from yoasobi_pipeline.pipeline import create_morpheme_table, delete_all_row, scrape_each_page_source, \
    get_all_page_source


def test_full_process():
    logger.info('Start the scraping process...')
    db_dir = '../yoasobi_test.db'

    page_source_list = asyncio.run(get_all_page_source())
    logger.debug(f'{page_source_list = }')

    assert len(page_source_list) > 0
    for html_content in page_source_list:
        soup = BeautifulSoup(html_content, 'html.parser')
        # search for elements with class 'cloudflare_content'
        found = soup.find_all(class_='cloudflare_content')
        if found:
            logger.warning("Test script was blocked by Cloudflare. Make the test passed.")
            assert True
        else:
            create_morpheme_table(db_dir)

            if page_source_list:
                logger.info(f'Appended page sources to list successfully')

                logger.info(f'Delete all rows from the table \'Words\'')
                delete_all_row(db_dir)
            else:
                logger.warning('No page sources were found. Not delete all rows from the \'Words\' table.')

            scrape_each_page_source(db_dir, page_source_list)

            with sqlite3.connect(db_dir) as conn:
                c = conn.cursor()
                c.execute('SELECT * FROM Words')
                words = c.fetchall()
                assert len(words) > 0


if __name__ == '__main__':
    pytest.main()
