from typing import Tuple, List

from loguru import logger

import yoasobi_project

logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {thread} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


class YoasobiScraper:
    def __init__(self, db_dir: str):
        """
        A 'YoasobiScraper' class creates or connects to the SQLite database when initialized.
        :param db_dir: SQLite database directory.
        """
        logger.info('Initializing SQLite database if not exist...')
        logger.info('Connect to the database if exist')
        self.db_dir = db_dir
        self.engine = yoasobi_project.connect_sqlite_db(db_dir)

    def main(self) -> None:
        """
        Main function that runs the web-scraping process and SQLite data migration.
        :return: None
        """
        logger.info('Start the scraping process...')

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

        self._scrape_each_page_source(page_source_list)

    def _scrape_each_page_source(self, page_source_list) -> None:
        """
        Scrape each page source.
        :param page_source_list: List of page sources.
        :return: None
        """
        logger.info('Scraping each page source...')
        for page_source in page_source_list:
            lyrics_list: list[str] = yoasobi_project.scrap(page_source)
            logger.debug(f'{lyrics_list = }')

            part_of_speech_list, romanized_words, song_name, words = self._extract_data(lyrics_list)

            yoasobi_project.insert_data(words, romanized_words, part_of_speech_list, song_name, self.db_dir)

            logger.debug(f'{len(words) = }')
            logger.debug(f'{len(romanized_words) = }')
            logger.debug(f'{len(part_of_speech_list) = }')

    @staticmethod
    def _extract_data(lyrics_list: list[str]) -> tuple[list[str], list[str], str, list[str]]:
        """
        Extract data from the page sources.
        :param lyrics_list: Lyrics list.
        :return: Tuple of Lists that contain extracted data from the page sources.
        """
        logger.info('Extracting data from the page sources...')
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

        return part_of_speech_list, romanized_words, song_name, words


if __name__ == '__main__':
    db_dir = 'yoasobi.db'
    YoasobiScraper(db_dir).main()

