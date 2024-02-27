"""
For storing and returning SQL queries.
"""
from loguru import logger


def drop_table() -> str:
    logger.info('Return drop table SQL query...')
    return '''
        DROP TABLE IF EXISTS Words;
    '''


def insert_data_query() -> str:
    logger.debug('Insert data SQL query...')
    return '''
    INSERT INTO Words (Kanji, Romanji, Part_of_Speech, Song, Song_Romanji, Timestamp) 
    VALUES (:Kanji, :Romanji, :Part_of_Speech, :Song, :Song_Romanji, :Timestamp)
    '''


def delete_all_rows() -> str:
    logger.info('Return delete all rows from table SQL query...')
    return '''
    DELETE FROM Words
    '''


def create_table_query() -> str:
    logger.info('Return create table SQL query...')
    return '''
            CREATE TABLE IF NOT EXISTS Words (
                ID INTEGER PRIMARY KEY,
                Kanji TEXT,
                Romanji TEXT,
                Part_of_Speech TEXT,
                Song TEXT,
                Song_Romanji TEXT,
                Timestamp TIMESTAMP
            );
    '''


if __name__ == '__main__':
    pass
