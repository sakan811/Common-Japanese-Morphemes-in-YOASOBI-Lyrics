import requests
from loguru import logger

import yoasobi_project

logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {thread} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


class Main:
    def __init__(self, db_dir: str):
        logger.info('Initializing SQLite database if not exist...')
        logger.info('Connect to the database if exist')
        self.db_dir = db_dir
        self.engine = yoasobi_project.connect_sqlite_db(db_dir)

    def main(self) -> None:
        """
        Main function that runs the web-scraping process and SQLite data migration.
        :return: None
        """
        try:
            urls: list[str] = yoasobi_project.return_url_list()

            page_source_list = yoasobi_project.thread_fetch_page_source(urls)

            yoasobi_project.connect_sqlite_db(self.db_dir)

            query = yoasobi_project.create_table_query()
            yoasobi_project.execute_sql_query(self.engine, query)

            if page_source_list:
                logger.info(f'Appended page sources to list successfully')

                logger.info(f'Delete all rows from the table \'Words\'')
                query = yoasobi_project.delete_all_rows()
                yoasobi_project.execute_sql_query(self.engine, query)
            else:
                logger.error('No page sources were found. Not delete all rows from the \'Words\' table.')

            for page_source in page_source_list:
                lyrics_list: list[str] = yoasobi_project.scrap(page_source)
                logger.debug(f'{lyrics_list = }')

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

                yoasobi_project.insert_data(words, romanized_words, part_of_speech_list, song_name, self.db_dir)

                logger.debug(f'{len(words) = }')
                logger.debug(f'{len(romanized_words) = }')
                logger.debug(f'{len(part_of_speech_list) = }')
        except Exception as e:
            logger.error(f'Error: {e}')


if __name__ == '__main__':
    # db_dir = 'yoasobi.db'
    # Main(db_dir).main()

    url = 'https://genius.com/Yoasobi-heart-beat-lyrics'
    response = requests.get(url)
    print(response.text)