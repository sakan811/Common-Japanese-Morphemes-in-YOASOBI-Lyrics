"""
For storing and returning SQL queries.
"""


def drop_table() -> str:
    return '''
        DROP TABLE IF EXISTS Words;
    '''


def insert_data_query() -> str:
    return '''
    INSERT INTO Words (Kanji, Romanji, Part_of_Speech, Song, Song_Romanji, Timestamp) 
    VALUES (:Kanji, :Romanji, :Part_of_Speech, :Song, :Song_Romanji, :Timestamp)
    '''


def delete_all_rows() -> str:
    return '''
    DELETE FROM Words
    '''


def delete_duplicates() -> str:
    return '''
    DELETE FROM Words
    WHERE ID NOT IN
        (
          SELECT MIN(ID) 
          FROM Words
          GROUP BY Song, Timestamp
        )
    '''


def create_table_query() -> str:
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


def update_part_of_speech_column() -> str:
    return '''
    UPDATE Words
    SET Part_of_Speech = 'Particle'
    WHERE Kanji = 'に';
    '''


def create_test_table() -> str:
    return '''
    CREATE TABLE Words_backup AS
    SELECT * FROM Words;
    '''


if __name__ == '__main__':
    pass
