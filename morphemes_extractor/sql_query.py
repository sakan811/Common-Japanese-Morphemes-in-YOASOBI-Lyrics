"""
For storing and returning SQL queries.
"""

from loguru import logger


def insert_data_query() -> str:
    """
    Return insert data into Words table SQL query.
    :return: SQL query
    """
    logger.debug("Insert data SQL query...")
    return """
    INSERT INTO Morpheme (Morpheme, Romanji, Part_of_Speech, Song, Song_Romanji, Timestamp) 
    VALUES (:Morpheme, :Romanji, :Part_of_Speech, :Song, :Song_Romanji, :Timestamp)
    """


def delete_all_rows() -> str:
    """
    Return deleting all rows from Words SQL query.
    :return: SQL query
    """
    logger.info("Return delete all rows from table SQL query...")
    return """
    DELETE FROM Morpheme;
    """


def create_morpheme_table_query() -> str:
    """
    Return create Morpheme table SQL query.
    :return: SQL query
    """
    logger.info("Return create table SQL query...")
    return """
            CREATE TABLE IF NOT EXISTS Morpheme (
                ID INTEGER PRIMARY KEY,
                Morpheme TEXT,
                Romanji TEXT,
                Part_of_Speech TEXT,
                Song TEXT,
                Song_Romanji TEXT,
                Timestamp TIMESTAMP
            );
    """


if __name__ == "__main__":
    pass
