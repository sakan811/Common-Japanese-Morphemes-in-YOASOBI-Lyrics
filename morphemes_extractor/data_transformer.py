import datetime
import pandas as pd
from morphemes_extractor.logger_config import setup_logger
import logging

# Set up logger
logger: logging.Logger = setup_logger(__name__)


def transform_data_to_df(
    char_list: list[str],
    romanized_char_list: list[str],
    part_of_speech_list: list[str],
    song_name: str,
    song_romanized_name: str,
) -> pd.DataFrame:
    """
    Transform data into a pandas dataframe.
    :param char_list: Japanese character list
    :param romanized_char_list: Romanized Japanese character list
    :param part_of_speech_list: Part of speech list
    :param song_name: Song's name in Japanese
    :param song_romanized_name: Song's name in Romanji
    :return: A pandas dataframe
    """
    logger.info("Transforming data into a pandas dataframe...")

    data = {
        "Morpheme": char_list,
        "Romanji": romanized_char_list,
        "Part_of_Speech": part_of_speech_list,
    }

    df = pd.DataFrame(data)
    df["Song"] = song_name
    df["Song_Romanji"] = song_romanized_name
    df["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df


if __name__ == "__main__":
    pass
