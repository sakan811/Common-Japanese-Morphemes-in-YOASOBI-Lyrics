import datetime
from loguru import logger
import pandas as pd

from scraper.data_extractor import extract_romanji


def transform_data_to_df(
        char_list: list[str],
        romanized_char_list: list[str],
        part_of_speech_list: list[str],
        song_name: str,
        is_morpheme: bool) -> pd.DataFrame:
    """
    Transform data into a pandas dataframe.
    :param char_list: Japanese character list
    :param romanized_char_list: Romanized Japanese character list
    :param part_of_speech_list: Part of speech list
    :param song_name: Song's name in Japanese
    :param is_morpheme: Whether the Japanese characters are morphemes.
    :return: A pandas dataframe
    """
    logger.info('Transforming data into a pandas dataframe...')

    if is_morpheme:
        data = {
            'Morpheme': char_list,
            'Romanji': romanized_char_list,
            'Part_of_Speech': part_of_speech_list
        }
    else:
        data = {
            'Word': char_list,
            'Romanji': romanized_char_list,
            'Part_of_Speech': part_of_speech_list
        }

    df = pd.DataFrame(data)
    df['Song'] = song_name
    df['Song_Romanji'] = extract_romanji(song_name)
    df['Timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df


if __name__ == '__main__':
    pass
