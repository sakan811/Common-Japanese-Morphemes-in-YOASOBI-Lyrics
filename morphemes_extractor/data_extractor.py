import logging
import pandas as pd
from cutlet import cutlet
from sudachipy import Tokenizer, dictionary, tokenizer
from typing import Dict, List, Tuple

from morphemes_extractor.logger_config import setup_logger
from morphemes_extractor.data_transformer import transform_data_to_df
from morphemes_extractor.json_utils import load_json
from morphemes_extractor.jp_data import MorphemeData
from morphemes_extractor.utils import check_list_len

# Set up logger
logger: logging.Logger = setup_logger(__name__)


# Constants for dictionary keys
TITLE_KEY = "title"
ROMANJI_TITLE_KEY = "romanji_title"
LYRICS_KEY = "lyrics"


def is_english(word: str) -> bool:
    """
    Check if the word is an English word.
    This function checks if all characters in the word are ASCII characters,
    which are typically used in English words.
    :param word: String. The word to check.
    :return: Boolean. True if the word consists only of ASCII characters, False otherwise.
    """
    return any(char.isalpha() and ord(char) < 128 for char in word)


def get_excluded_pos_dict() -> dict[str, str]:
    """
    Get Excluded Part of Speech Dictionary.
    :return: Excluded Part of Speech Dictionary.
    """
    logger.info("Get excluded Part of Speech dictionary...")
    return {
        "空白": "Whitespace",
        "補助記号": "Supplementary Symbol",
        "連体詞": "Adnominal",
    }


def extract_morphemes_from_lyrics(lyrics: str) -> list[str]:
    """
    Extract morphemes from the lyrics.
    Remove white space.
    Exclude English words, Integer, and Japanese Auxiliary Symbols.
    :param lyrics: String
    :return: List[String]
    """
    logger.info("Extract words from lyrics...")
    excluded_jp_pos_tags = get_excluded_pos_dict()

    logger.info("Create tokenizer")
    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    logger.info("Use Tokenizer Mode C")
    mode = tokenizer.Tokenizer.SplitMode.C

    logger.info(
        "Create words list by adding words into 'words' list if word is not in 'excluded_jp_pos_tags'"
    )
    words = [
        m.dictionary_form()
        for m in tokenizer_obj.tokenize(lyrics, mode)
        if m.part_of_speech()[0] not in excluded_jp_pos_tags
    ]

    logger.info("Remove newline characters and whitespace")
    words = [word.strip() for word in words if word.strip()]

    logger.info("Exclude English words")
    words = [word for word in words if not is_english(word)]

    logger.info("Exclude Integer")
    words = [word for word in words if not word.isdigit()]
    return words


def get_jp_pos_dict() -> dict[str, str]:
    """
    Get the Japanese Part of Speech dictionary.
    :return: Japanese Part of Speech dictionary.
    """
    logger.info("Get the Japanese Part of Speech dictionary...")
    return {
        "代名詞": "Pronoun",
        "副詞": "Adverb",
        "助動詞": "Auxiliary Verb",
        "助詞": "Particle",
        "動詞": "Verb",
        "名詞": "Noun",
        "形容詞": "Adjective",
        "形状詞": "Adjectival Noun",
        "感動詞": "Interjection",
        "接尾辞": "Suffix",
        "接続詞": "Conjunction",
        "接頭辞": "Prefix",
    }


def extract_part_of_speech_from_morphemes(morpheme_list: list[str]) -> list[str]:
    """
    Extract Part of Speech from the morpheme list.
    Exclude English words and Japanese Auxiliary Symbols.
    :param morpheme_list: Japanese morpheme list as List of String.
    :return: List[String]
    """
    logger.info("Extract part of speech from morpheme list...")
    jp_pos_tags = get_jp_pos_dict()

    logger.info("Create tokenizer")
    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    logger.info("Mode C")
    mode = tokenizer.Tokenizer.SplitMode.C

    logger.info(
        "Create part of speech list by extracting part of speech from morpheme list"
    )
    part_of_speech_list: list[str] = []
    for word in morpheme_list:
        tokenized_word = tokenizer_obj.tokenize(word, mode)
        part_of_speech = tokenized_word[0].part_of_speech()
        part_of_speech_list.append(part_of_speech[0])

    logger.info("Translate part of speech from Japanese to English and assign to list")
    part_of_speech_list = [
        jp_pos_tags[part_of_speech]
        for part_of_speech in part_of_speech_list
        if part_of_speech in jp_pos_tags
    ]

    return part_of_speech_list


def extract_romanji_from_jp_characters(jp_characters: list[str]) -> list[str]:
    """
    Extract Romanji from a Japanese characters within the list.
    :param jp_characters: List of Japanese characters.
    :return: List[String]
    """
    logger.info("Extract romanjis from characters list...")
    return [extract_romanji(jp_char) for jp_char in jp_characters]


def extract_romanji(jp_char: str) -> str:
    """
    Extract Romanji from Japanese words.
    :param jp_char: Japanese character.
    :return: Romanji.
    """
    return cutlet.Cutlet().romaji(jp_char)  # type: ignore


def extract_data(
    song: Dict[str, str],
) -> Tuple[List[str], List[str], List[str], str, str]:
    """
    Extract data from the JSON file.
    :param song: YOASOBI song.
    :return: Tuple of extracted data from the JSON file.
    """
    song_name: str = song[TITLE_KEY]
    logger.info(f"Extracting data from song {song_name}...")

    song_eng_name: str = song[ROMANJI_TITLE_KEY]
    lyrics: str = song[LYRICS_KEY]

    morphemes: List[str] = extract_morphemes_from_lyrics(lyrics)
    logger.debug(f"morphemes list: {morphemes}")

    romanized_morphemes: List[str] = extract_romanji_from_jp_characters(morphemes)

    part_of_speech_list: List[str] = extract_part_of_speech_from_morphemes(morphemes)

    morpheme_data = MorphemeData(morphemes, romanized_morphemes, part_of_speech_list)
    list_len = check_list_len(morpheme_data)
    words_len = list_len[0]
    romanized_words_len = list_len[1]
    part_of_speech_list_len = list_len[2]

    if words_len == romanized_words_len == part_of_speech_list_len:
        logger.info(
            "The length of words, romanized_morphemes, and part_of_speech_list are equal."
        )
        return (
            morpheme_data.morphemes,
            morpheme_data.romanized_morphemes,
            morpheme_data.part_of_speech_list,
            song_name,
            song_eng_name,
        )
    else:
        logger.warning(
            "The length of words, romanized_morphemes, and part_of_speech_list are not equal."
        )
        raise ValueError(
            "The length of words, romanized_morphemes, and part_of_speech_list are not equal."
        )


def get_song_list(json_data: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    """
    Get the list of songs from the JSON data.
    :param json_data: JSON data
    :return: List of songs
    """
    song_list: list[dict[str, str]] = json_data["songs"]
    return song_list


def get_morphemes_from_songs(json_path_list: list[str]) -> pd.DataFrame:
    """
    Extract morphemes and related information from songs in JSON files.

    :param json_path_list: List of paths to JSON files containing song data.
    :return: DataFrame with columns: morphemes, romanized morphemes,
             parts of speech, song names, and romanized song names.
             Returns empty DataFrame if no valid data is found.
    """
    json_data = load_json(json_path_list)
    song_list = get_song_list(json_data)
    df_list: list[pd.DataFrame] = []
    for song in song_list:
        (
            morphemes,
            romanized_morphemes,
            part_of_speech_list,
            song_name,
            song_romanized_name,
        ) = extract_data(song)
        df = transform_data_to_df(
            morphemes,
            romanized_morphemes,
            part_of_speech_list,
            song_name,
            song_romanized_name,
        )
        if not df.empty:
            df_list.append(df)

    df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
    return df
