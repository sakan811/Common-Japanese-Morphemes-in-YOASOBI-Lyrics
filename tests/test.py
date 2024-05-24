import random
import sqlite3
import time

import requests
import pytest
from bs4 import BeautifulSoup
from loguru import logger

import yoasobi_project


def get_html_preparation():
    # List of user agents to rotate
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        # Add more user agents as needed
    ]

    # Function to fetch URL with headers and handle cookies
    def fetch_url(url, session):
        headers = {
            "User-Agent": random.choice(user_agents)
        }
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    # URL you want to fetch
    url = "https://genius.com/Yoasobi-heart-beat-lyrics"

    # Create a session to persist cookies
    session = requests.Session()

    content = None

    # Fetch the URL with retries and random delays
    for attempt in range(5):  # Retry up to 5 times
        try:
            print(f"Attempt {attempt + 1}: Fetching {url}")
            content = fetch_url(url, session)
            print("Fetched successfully.")
            # Add your logic to process the content here
            break  # Exit loop if successful
        except requests.exceptions.HTTPError as e:
            print(e)
            # Wait for a random time between 60 and 120 seconds before retrying
            time.sleep(random.uniform(60, 120))

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            # Wait for a random time between 60 and 120 seconds before retrying
            time.sleep(random.uniform(60, 120))

    return content

def test_full_process():
    # with open('tests/html_test.html', 'r', encoding='utf-8') as file:
    #     html_content = file.read()

    # url = 'https://genius.com/Yoasobi-heart-beat-lyrics'
    #
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    # }
    # response = requests.get(url, headers=headers)
    # response.raise_for_status()

    html_content = get_html_preparation()

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

    db_dir = '../yoasobi_test.db'

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
    pytest.main()
