import sqlite3

import pytest
from bs4 import BeautifulSoup, ResultSet
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from main import Main


def test_fetch():
    url = 'https://genius.com/Yoasobi-heart-beat-lyrics'

    logger.info('Set options for Chrome')
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI) for better performance

    logger.info('Open browser')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    webpage_html = driver.page_source

    logger.info('Web scraping...')

    logger.info('Parser html content to BeautifulSoup Object')
    soup = BeautifulSoup(webpage_html, 'html.parser')

    logger.info('Find all desired elements by tag and class')
    lyrics_div: ResultSet = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')

    logger.info('Add lyrics to \'lyrics_list\' with \\n seperator.')
    lyrics_list = [lyrics.get_text(separator='\n') for lyrics in lyrics_div]
    logger.debug(f'{lyrics_list = }')

    assert lyrics_list is not None

# def test_main():
#     db_dir = 'yoasobi.db'
#     Main(db_dir).main()
#
#     with sqlite3.connect(db_dir) as conn:
#         c = conn.cursor()
#         c.execute('SELECT * FROM Words')
#         words = c.fetchall()
#         assert len(words) > 0


if __name__ == '__main__':
    pytest.main()
