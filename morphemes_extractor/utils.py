from bs4 import BeautifulSoup
from loguru import logger


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
    pass
