import asyncio
import aiohttp

from bs4 import BeautifulSoup, ResultSet
from loguru import logger


def return_url_list() -> list[str]:
    logger.info('Return URL list...')
    return [
        'https://genius.com/Yoasobi-yuusha-lyrics',
        'https://genius.com/Yoasobi-the-blessing-lyrics',
        'https://genius.com/Yoasobi-umi-no-manimani-lyrics',
        'https://genius.com/Yoasobi-mr-lyrics',
        'https://genius.com/Yoasobi-idol-lyrics',
        'https://genius.com/Yoasobi-seventeen-lyrics',
        'https://genius.com/Yoasobi-adventure-lyrics',
        'https://genius.com/Yoasobi-sukida-lyrics',
        'https://genius.com/Yoasobi-biri-biri-lyrics',
        'https://genius.com/Yoasobi-tsubame-lyrics',
        'https://genius.com/Yoasobi-rgb-lyrics',
        'https://genius.com/Yoasobi-romance-lyrics',
        'https://genius.com/Yoasobi-mou-sukoshi-dake-lyrics',
        'https://genius.com/Yoasobi-comet-lyrics',
        'https://genius.com/Yoasobi-monster-lyrics',
        'https://genius.com/Yoasobi-moshimo-inochiga-egaketara-lyrics',
        'https://genius.com/Yoasobi-loveletter-lyrics',
        'https://genius.com/Yoasobi-encore-lyrics',
        'https://genius.com/Yoasobi-harujion-lyrics',
        'https://genius.com/Yoasobi-ano-yume-wo-nazotte-lyrics',
        'https://genius.com/Yoasobi-probably-tabun-lyrics',
        'https://genius.com/Yoasobi-gunjou-lyrics',
        'https://genius.com/Yoasobi-haruka-lyrics',
        'https://genius.com/Yoasobi-yoru-ni-kakeru-lyrics',
        'https://genius.com/Yoasobi-heart-beat-lyrics',
        'https://genius.com/Yoasobi-undead-lyrics'
    ]


async def async_fetch_page_source(url: str) -> bytes:
    """
    Asynchronously fetch a page source from URL.
    :param url: Page URL.
    :return: Page source.
    """
    logger.info(f'Fetching the page content from {url}...')

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f'Failed to fetch the page: {response.status}')
            else:
                logger.info(f'Successfully fetched the page: {url}')
                html_content = await response.read()
                return html_content


async def async_fetch_page_sources(urls: list[str]) -> list[bytes]:
    """
    Asynchronously fetch page sources using aiohttp.
    :param urls: URL list.
    :return: List of page sources.
    """
    logger.info('Fetching page sources asynchronously...')

    async def fetch_with_error_handling(url):
        try:
            return await async_fetch_page_source(url)
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    tasks = [fetch_with_error_handling(url) for url in urls]
    page_sources = await asyncio.gather(*tasks)

    return list(page_sources)


def get_lyrics_list(page_source_list: list[bytes]) -> list[list[str]]:
    """
    Scrape each page source.
    :param page_source_list: List of page sources.
    :return: Tuple of scraped data.
    """
    logger.info('Getting a lyrics list from \'page_source_list\'...')
    lyrics_list = []
    for page_source in page_source_list:
        lyrics_list.append(scrape(page_source))
    return lyrics_list


def scrape(page_source: bytes) -> list[str]:
    """
    Scrape an element of the URL.
    :param page_source: Page source to be scraped.
    :return: List of extracted lyrics.
    """
    logger.info('Web scraping...')

    logger.info('Parser html content to BeautifulSoup Object')
    soup = BeautifulSoup(page_source, 'html.parser')

    logger.info('Find all desired elements by tag and class')
    lyrics_div: ResultSet = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')

    logger.info('Add lyrics to \'lyrics_list\' with \\n seperator.')
    lyrics_list = [lyrics.get_text(separator='\n') for lyrics in lyrics_div]

    return lyrics_list


if __name__ == '__main__':
    pass
