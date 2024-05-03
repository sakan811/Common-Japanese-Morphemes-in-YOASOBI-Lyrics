from loguru import logger


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


if __name__ == '__main__':
    pass
