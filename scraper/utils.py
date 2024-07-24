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


def fetch_html_content_for_test(test_html: str) -> list[bytes]:
    """
    Fetch an HTML page source for testing purposes.
    :param test_html: The HTML content for testing.
    :return: List of HTML content.
    """
    logger.info('Fetching HTML page...')

    # Read the HTML file as bytes
    with open(test_html, 'rb') as file:
        content_bytes = file.read()
    # Decode bytes to string
    content_str = content_bytes.decode('utf-8')
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content_str, 'html.parser')
    # Convert BeautifulSoup object back to HTML string
    pagesource = str(soup)
    # Encode the HTML string back to bytes
    page_source_bytes = pagesource.encode('utf-8')
    # Create a list of bytes
    page_source_list = [page_source_bytes]
    return page_source_list


if __name__ == '__main__':
    pass
