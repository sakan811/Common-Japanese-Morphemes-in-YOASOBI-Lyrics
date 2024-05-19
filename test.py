import sqlite3
import time

import pytest
from bs4 import BeautifulSoup, ResultSet
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import yoasobi_project


def test_full_process():
    url = 'https://genius.com/Yoasobi-heart-beat-lyrics'

    logger.info('Set options for Chrome')
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    logger.info('Open browser')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    time.sleep(20)

    webpage_html = driver.page_source

    logger.info('Web scraping...')

    logger.info('Parser html content to BeautifulSoup Object')
    soup = BeautifulSoup(webpage_html, 'html.parser')

    logger.info('Find all desired elements by tag and class')
    lyrics_div: ResultSet = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')
    logger.debug(f'{lyrics_div = }')

    logger.info('Add lyrics to \'lyrics_list\' with \\n seperator.')
    lyrics_list = [lyrics.get_text(separator='\n') for lyrics in lyrics_div]
    logger.debug(f'{lyrics_list = }')

    assert lyrics_list != []

    song_name: str = yoasobi_project.extract_song_name_from_lyrics_list(lyrics_list)
    logger.debug(f'{song_name = }')

    lyrics: str = yoasobi_project.extract_lyrics_from_lyrics_list(lyrics_list)
    logger.debug(f'{lyrics = }')

    words: list[str] = yoasobi_project.extract_words_from_lyrics(lyrics)
    logger.debug(f'{words = }')

    romanized_words: list[str] = yoasobi_project.extract_romanji_from_words(words)
    logger.debug(f'{romanized_words = }')

    part_of_speech_list: list[str] = yoasobi_project.extract_part_of_speech_from_words(words)
    logger.debug(f'{part_of_speech_list = }')

    db_dir = 'yoasobi_test.db'

    yoasobi_project.connect_sqlite_db(db_dir)

    engine = yoasobi_project.connect_sqlite_db(db_dir)

    query = yoasobi_project.create_table_query()
    yoasobi_project.execute_sql_query(engine, query)

    logger.info(f'Delete all rows from the table \'Words\'')
    query = yoasobi_project.delete_all_rows()
    yoasobi_project.execute_sql_query(engine, query)

    yoasobi_project.insert_data(words, romanized_words, part_of_speech_list, song_name, db_dir)

    logger.debug(f'{len(words) = }')
    logger.debug(f'{len(romanized_words) = }')
    logger.debug(f'{len(part_of_speech_list) = }')

    with sqlite3.connect(db_dir) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Words')
        words = c.fetchall()
        assert len(words) > 0


if __name__ == '__main__':
    pytest.main(args=['--html=pytest_report.html', '--self-contained-html'])
