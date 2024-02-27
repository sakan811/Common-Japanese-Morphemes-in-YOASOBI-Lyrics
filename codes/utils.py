from sqlalchemy import Engine
from loguru import  logger

from codes import sql_query as sqlquery
from codes import sqlite_db as sqldb


def insert_lyrics() -> str:
    """
    Prompt the user to enter lyrics line by line until they press Ctrl+D.
    :return: A string containing the entered lyrics.
    """
    print(f'Enter lyrics. Ctrl+D after finish.')
    lyrics = []
    logger.info('Prompt the user to enter lyrics line by line until they press Ctrl+D')
    while True:
        try:
            lyrics_line: str = input()
        except EOFError as e:
            logger.error(f'Ctrl + D was pressed. EOFError: {e}.')
            break
        logger.info(f'Add {lyrics_line = } to \'lyrics\' list')
        lyrics.append(lyrics_line)
    logger.info('Join \'lyrics_line\' in \'lyrics\' list together')
    lyrics_joined: str = ''.join(lyrics)
    return lyrics_joined


def choose_table_options() -> str | None:
    """
    Allows the user to choose from various table options related to the database \n
    Options: \n
    1: Drop table: Drops the entire table from the database. \n
    2: Create table: Creates a new table in the database. \n
    3: Drop all rows in the table: Deletes all rows from the table, but keeps the table structure intact. \n
    4: Skip: Skips performing any action on the table. \n
    :return: If there is a SQL query corresponding to the chosen option, return String, else return None.
    """
    logger.info('Prompting the user to choose from various table options related to the database')
    while True:
        print(f'Drop table: press 1 \n'
              f'Create table: press 2 \n'
              f'Drop all rows in the table: press 3 \n'
              f'Skip: press 4')
        option: str = input()
        logger.debug(f'{option = }')
        if option == '1':
            print(f'You chose to drop the table. \n'
                  f'Sure? \n'
                  f'Press 1 to cancel \n'
                  f'Press 2 to continue')
            logger.info('User chose to drop the table')
            not_cancel = True
            logger.debug(f'{not_cancel = }')
            while not_cancel:
                user_answer = input()
                logger.debug(f'{user_answer = }')
                if user_answer == '1':
                    logger.info('Cancel drop table')
                    not_cancel = False
                    logger.debug(f'{not_cancel = }')
                elif user_answer == '2':
                    logger.info('Drop table')
                    return sqlquery.drop_table()
                else:
                    logger.warning('Invalid input')
                    print(f'Invalid Input')
        elif option == '2':
            print(f'You chose to create the table.')
            logger.info('User chose to create the table')
            return sqlquery.create_table_query()
        elif option == '3':
            print(f'You chose to drop all rows in the table. \n'
                  f'Sure? \n'
                  f'Press 1 to cancel \n'
                  f'Press 2 to continue')
            logger.info('User chose to drop all rows in the table')
            not_cancel = True
            logger.debug(f'{not_cancel = }')
            while not_cancel:
                user_answer = input()
                logger.debug(f'{user_answer = }')
                if user_answer == '1':
                    not_cancel = False
                    logger.debug(f'{not_cancel = }')
                elif user_answer == '2':
                    logger.info('Delte all rows from table')
                    return sqlquery.delete_all_rows()
                else:
                    logger.warning('Invalid Input')
                    print(f'Invalid Input')
        elif option == '4':
            logger.info('User skipped')
            print(f'Skipped')
            return
        else:
            logger.warning('Invalid input')
            print(f'Invalid input')


def check_table_sql_query(option_result: str | None, sqlite_db: Engine) -> bool | None:
    """
    Check if there is any sql query chosen by the user.
    :param option_result: Result of the user whether they want to Drop or Create the table.
                        If they chose to deal with the table, then the param is String,
                        if not, then the param is None.
    :param sqlite_db: sqlalchemy Engine Object
    :return: If param option_result is String then return True, else return None.
    """
    logger.info(f'Check if {option_result = } is string')
    if isinstance(option_result, str):
        sql_query: str = option_result
        logger.debug(f'{sql_query = }')
        logger.info(f'Execute {sql_query = }')
        sqldb.execute_sql_query(sqlite_db, sql_query)
        sql_query_exist = True
        logger.debug(f'{sql_query_exist = }')
        print(f'SQL query executed.')
        return sql_query_exist
    else:
        logger.info('No any SQL query was parsed')
        print(f'No any SQL query was parsed.')


if __name__ == '__main__':
    pass
