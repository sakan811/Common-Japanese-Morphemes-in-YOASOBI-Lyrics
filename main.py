from loguru import logger

from yoasobi_pipeline.pipeline import get_all_page_source, create_table_if_not_exist, delete_all_row, \
    scrape_each_page_source

logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def start_pipeline(db_dir: str) -> None:
    """
    Start a pipeline that web-scraping YOASOBI's songs' lyrics from Genius.com
    :param db_dir: Database directory.
    :return: None
    """
    logger.info('Start the scraping process...')

    page_source_list = get_all_page_source()

    create_table_if_not_exist(db_dir)

    if page_source_list:
        logger.info(f'Appended page sources to list successfully')

        logger.info(f'Delete all rows from the table \'Words\'')
        delete_all_row(db_dir)
    else:
        logger.warning('No page sources were found. Not delete all rows from the \'Words\' table.')

    scrape_each_page_source(db_dir, page_source_list)


if __name__ == '__main__':
    db_dir = 'yoasobi.db'
    start_pipeline(db_dir)
