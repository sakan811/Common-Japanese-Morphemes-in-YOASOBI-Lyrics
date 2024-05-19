import os
import sqlite3

import pytest
import requests
from bs4 import BeautifulSoup
from loguru import logger

import yoasobi_project


def test_full_process():
    # Define the login URL
    login_url = 'https://genius.com/login'

    # Define your credentials
    genius_username = os.environ.get('GENIUS_USERNAME')
    genius_password = os.environ.get('GENIUS_PASSWORD')

    # Create a session
    session = requests.Session()

    # Send a POST request with credentials to the login endpoint
    login_data = {
        'username': genius_username,
        'password': genius_password
    }
    response = session.post(login_url, data=login_data)
    page_response = None
    # Check if login was successful
    if response.status_code == 200:
        logger.info("Login successful!")
        # Navigate to the desired page after successful login
        page_url = 'https://genius.com/Yoasobi-heart-beat-lyrics'
        page_response = session.get(page_url)
        # Check if page retrieval was successful
        if page_response.status_code == 200:
            logger.info(f"Successfully fetched the page: {page_url}")
            # Now you can work with the page content
            logger.info(page_response.text)
        else:
            logger.info(f"Failed to fetch the page: {page_response.status_code}")
    else:
        logger.info(f"Failed to login: {response.status_code}")

    html_content = page_response.content

    logger.info('Parsing HTML content to BeautifulSoup Object')
    soup = BeautifulSoup(html_content, 'html.parser')

    logger.info('Finding all desired elements by tag and class')
    lyrics_div = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')
    logger.debug(f'Number of lyrics divs found: {len(lyrics_div)}')

    logger.info("Adding lyrics to 'lyrics_list' with \\n separator.")
    lyrics_list = [lyrics.get_text(separator='\n') for lyrics in lyrics_div]
    logger.debug(f'lyrics_list length = {len(lyrics_list)}')
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
