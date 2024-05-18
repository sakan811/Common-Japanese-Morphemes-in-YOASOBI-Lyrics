import re
from selenium_stealth import stealth
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup, ResultSet
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
        'https://genius.com/Yoasobi-heart-beat-lyrics'
    ]


def extract_song_name_from_lyrics_list(lyrics_list: list[str]) -> str:
    """
    Extract song name from the 'lyrics_list'.
    :param lyrics_list: List of lyrics of the song.
    :return: Song\'s name.
    """
    logger.info('Extract song name...')
    logger.info('Access 0th element in \'lyrics_list\' ')
    first_element_lyrics_list: str = lyrics_list[0]
    logger.debug(f'{first_element_lyrics_list = }')

    first_element_split: list[str] = first_element_lyrics_list.split()
    logger.debug(f'{first_element_split = }')

    logger.info('Extracting the song name from the \'first_element_split\'. '
                'Accessing the text between the Japanese quotation marks.')
    song_name = first_element_split[0].split('「')[1:][0].split('」')[0]

    return song_name


def extract_lyrics_from_lyrics_list(lyrics_list: list[str]) -> str:
    """
    Extract lyrics from the 'lyrics_list'
    :param lyrics_list: List containing lyrics of the song
    :return: Song's lyrics
    """
    logger.info('Extract lyrics...')
    logger.info('Strip lyrics from \'lyrics_list\' and turn them into list')
    lyrics_list: list[str] = [lyrics.strip() for lyrics in lyrics_list]
    logger.debug(f'{lyrics_list = }')

    logger.info('Join elements in \'lyrics_list\'')
    lyrics: str = ''.join(lyrics_list)

    logger.info('Split lyrics and exclude 0th element')
    lyrics_list: list[str] = lyrics.split()[1:]

    logger.info('Join elements in \'lyrics_list\'')
    lyrics: str = ''.join(lyrics_list)

    logger.info('Use regular expression to remove characters within square brackets and the brackets themselves')
    lyrics: str = re.sub(r'\[.*?]', '', lyrics)
    return lyrics


def fetch_page_source(url: str, page_source_list) -> None:
    """
    Fetch a page source from the URL.
    :param page_source_list: Page source list.
    :param url: Page's URL.
    :return: Page source as String.
    """
    logger.info('Fetching page source...')

    logger.info('Set Chrome options')
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    logger.info('Open browser')
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    logger.info(f'Open web page: {url}')

    driver.get(url)

    webpage_html = driver.page_source

    logger.info('Close the driver')
    driver.quit()

    if webpage_html:
        logger.info('Retrieved page source successfully')
        page_source_list.append(webpage_html)
    else:
        logger.error('Retrieved page source failed')


def thread_fetch_page_source(urls: list[str]) -> list[str]:
    """
    Fetch a page source from a URL list using ThreadPoolExecutor.
    :param urls: List of URLs.
    :return: List of page sources as String.
    """
    logger.info('Fetching page source from URL list using ThreadPoolExecutor...')
    page_source_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        logger.info('Submit all tasks to the executor')
        futures = [executor.submit(fetch_page_source, url, page_source_list) for url in urls]

        logger.info('Wait for all tasks to complete')
        for future in futures:
            future.result()

        if page_source_list:
            logger.info('Appended page source to the list successfully')
            return page_source_list
        else:
            logger.error('Page source list is empty')


def scrap(url: str) -> list[str]:
    """
    Scrape an element of the URL.
    :param url: URL to be scraped.
    :return: List of extracted lyrics.
    """
    logger.info('Web scraping...')

    logger.info('Parser html content to BeautifulSoup Object')
    soup = BeautifulSoup(url, 'html.parser')

    logger.info('Find all desired elements by tag and class')
    class_name = 'Lyrics__Container-sc-1ynbvzw-1 kUgSbL'
    lyrics_div: ResultSet = soup.find_all('div', class_=class_name)

    if lyrics_div:
        logger.info(f'Found lyrics elements by {class_name = } successfully')
    else:
        logger.error(f'No lyrics elements found by {class_name = }')

    logger.info('Add lyrics to \'lyrics_list\' with \\n seperator.')
    lyrics_list = [lyrics.get_text(separator='\n') for lyrics in lyrics_div]

    return lyrics_list


if __name__ == '__main__':
    pass
