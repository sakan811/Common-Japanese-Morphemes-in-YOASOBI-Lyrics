import re

from cutlet import cutlet
from sudachipy import Tokenizer, dictionary, tokenizer
from loguru import logger

from scraper.utils import check_list_len


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
        "連体詞": "Adnominal"
    }


def extract_morphemes_from_lyrics(lyrics: str) -> list[str]:
    """
    Extract morphemes from the lyrics.
    Remove white space.
    Exclude English words, Integer, and Japanese Auxiliary Symbols.
    :param lyrics: String
    :return: List[String]
    """
    logger.info('Extract words from lyrics...')
    excluded_jp_pos_tags = get_excluded_pos_dict()

    logger.info('Create tokenizer')
    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    logger.info('Use Tokenizer Mode C')
    mode = tokenizer.Tokenizer.SplitMode.C

    logger.info('Create words list by adding words into \'words\' list if word is not in \'excluded_jp_pos_tags\'')
    words = [m.dictionary_form() for m in tokenizer_obj.tokenize(lyrics, mode) if
             m.part_of_speech()[0] not in excluded_jp_pos_tags]

    logger.info('Remove newline characters and whitespace')
    words = [word.strip() for word in words if word.strip()]

    logger.info('Exclude English words')
    words = [word for word in words if not is_english(word)]

    logger.info('Exclude Integer')
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
    logger.info('Extract part of speech from morpheme list...')
    jp_pos_tags = get_jp_pos_dict()

    logger.info('Create tokenizer')
    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    logger.info('Mode C')
    mode = tokenizer.Tokenizer.SplitMode.C

    logger.info('Create part of speech list by extracting part of speech from morpheme list')
    part_of_speech_list = []
    for word in morpheme_list:
        tokenized_word = tokenizer_obj.tokenize(word, mode)
        part_of_speech = tokenized_word[0].part_of_speech()
        part_of_speech_list.append(part_of_speech[0])

    logger.info('Translate part of speech from Japanese to English and assign to list')
    part_of_speech_list = [jp_pos_tags[part_of_speech] for part_of_speech in part_of_speech_list if
                           part_of_speech in jp_pos_tags]

    return part_of_speech_list


def extract_romanji_from_jp_characters(jp_characters: list[str]) -> list[str]:
    """
    Extract Romanji from a Japanese characters within the list.
    :param jp_characters: List of Japanese characters.
    :return: List[String]
    """
    logger.info('Extract romanjis from characters list...')
    return [extract_romanji(jp_char) for jp_char in jp_characters]


def extract_romanji(jp_char: str) -> str:
    """
    Extract Romanji from Japanese words.
    :param jp_char: Japanese character.
    :return: Romanji.
    """
    return cutlet.Cutlet().romaji(jp_char)


def extract_data(lyrics_list: list[str]) -> tuple[list[str], list[str], list[str], str]:
    """
    Extract data from the page sources.
    :param lyrics_list: Lyrics list.
    :return: Tuple of extracted data from the page sources.
    """
    logger.info('Extracting data from the page sources...')
    song_name: str = extract_song_name_from_lyrics_list(lyrics_list)

    lyrics: str = extract_lyrics_from_lyrics_list(lyrics_list)

    morphemes: list[str] = extract_morphemes_from_lyrics(lyrics)

    romanized_words: list[str] = extract_romanji_from_jp_characters(morphemes)

    part_of_speech_list: list[str] = extract_part_of_speech_from_morphemes(morphemes)

    list_len = check_list_len(morphemes, romanized_words, part_of_speech_list)
    words_len = list_len[0]
    romanized_words_len = list_len[1]
    part_of_speech_list_len = list_len[2]

    if words_len == romanized_words_len == part_of_speech_list_len:
        logger.info("The length of words, romanized_words, and part_of_speech_list are equal.")
        return morphemes, romanized_words, part_of_speech_list, song_name
    else:
        raise Exception('The length of words, romanized_words, and part_of_speech_list are not equal.')


def extract_song_name_from_lyrics_list(lyrics_list: list[str]) -> str:
    """
    Extract song name from the 'lyrics_list'
    :param lyrics_list: List of lyrics of the song
    :return: Song\'s name
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
    Extract lyrics from the 'lyrics_list'.
    :param lyrics_list: List containing lyrics of the song.
    :return: Song's lyrics.
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


if __name__ == '__main__':
    pass
