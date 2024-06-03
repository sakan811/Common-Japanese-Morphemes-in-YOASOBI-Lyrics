from loguru import logger

import yoasobi_project

logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
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
            logger.warning('No page sources were found. Not delete all rows from the \'Words\' table.')

        self.scrape_each_page_source(page_source_list)

    def scrape_each_page_source(self, page_source_list) -> None:
        """
        Scrape each page source.
        :param page_source_list: List of page sources.
        :return: Tuple of scraped data.
        """
        logger.info('Scraping each page source...')
        for page_source in page_source_list:
            lyrics_list: list[str] = yoasobi_project.scrap(page_source)

            words, romanized_words, part_of_speech_list, song_name = extract_data(lyrics_list)

            yoasobi_project.insert_data(words, romanized_words, part_of_speech_list, song_name, self.db_dir)


def extract_data(lyrics_list: list[str]) -> tuple:
    """
    Extract data from the page sources.
    :param lyrics_list: Lyrics list.
    :return: Tuple of extracted data from the page sources.
    """
    logger.info('Extracting data from the page sources...')
    song_name: str = yoasobi_project.extract_song_name_from_lyrics_list(lyrics_list)

    lyrics: str = yoasobi_project.extract_lyrics_from_lyrics_list(lyrics_list)

    words: list[str] = yoasobi_project.extract_words_from_lyrics(lyrics)

    romanized_words: list[str] = yoasobi_project.extract_romanji_from_words(words)

    part_of_speech_list: list[str] = yoasobi_project.extract_part_of_speech_from_words(words)

    list_len = check_list_len(words, romanized_words, part_of_speech_list)
    words_len = list_len[0]
    romanized_words_len = list_len[1]
    part_of_speech_list_len = list_len[2]

    if words_len != romanized_words_len or words_len != part_of_speech_list_len:
        raise Exception('The length of words, romanized_words, and part_of_speech_list are not equal.')

    return words, romanized_words, part_of_speech_list, song_name


def check_list_len(*args) -> tuple:
    """
    Calculate the length of the target list and return it as an integer.
    :param args: Target lists.
    :return: Length of the target list as Tuple.
    """
    logger.info(f"Checking length of target lists...")
    lengths = [len(arg) for arg in args]
    return tuple(lengths)


if __name__ == '__main__':
    db_dir = 'yoasobi.db'
    YoasobiScraper(db_dir).main()
