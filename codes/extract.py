from cutlet import cutlet
from sudachipy import Tokenizer, dictionary, tokenizer
from loguru import logger


def is_english(word: str) -> bool:
    """
    Check if the word is an English word.
    This function checks if all characters in the word are ASCII characters,
    which are typically used in English words.
    :param word: String. The word to check.
    :return: Boolean. True if the word consists only of ASCII characters, False otherwise.
    """
    return any(char.isalpha() and ord(char) < 128 for char in word)


def insert_excluded_pos() -> dict[str, str]:
    return {
        '補助記号': 'Auxiliary Symbols'
    }


def extract_words_from_lyrics(lyrics: str) -> list[str]:
    """
    Extract words from the lyrics.
    Remove white space.
    Exclude English words, Integer, and Japanese Auxiliary Symbols.
    :param lyrics: String
    :return: List[String]
    """
    excluded_jp_pos_tags = insert_excluded_pos()
    logger.debug(f'{excluded_jp_pos_tags = }')

    logger.info('Create tokenizer')
    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    logger.info('Mode C')
    mode = tokenizer.Tokenizer.SplitMode.C

    logger.info('Create words list by adding words into \'words\' list if word is not in \'excluded_jp_pos_tags\'')
    words = [m.surface() for m in tokenizer_obj.tokenize(lyrics, mode) if
             m.part_of_speech()[0] not in excluded_jp_pos_tags]

    logger.info('Remove newline characters and whitespace')
    words = [word.strip() for word in words if word.strip()]

    logger.info('Exclude English words')
    words = [word for word in words if not is_english(word)]

    logger.info('Exclude Integer')
    words = [word for word in words if not word.isdigit()]
    return words


def extract_part_of_speech_from_words(word_list: list[str]) -> list[str]:
    """
    Extract Part of Speech from the word list.
    Exclude English words and Japanese Auxiliary Symbols.
    :param word_list: Japanese word list as List of String.
    :return: List[String]
    """
    jp_pos_tags = {
        '代名詞': 'Pronoun',
        '副詞': 'Adverb',
        '助動詞': 'Auxiliary verb',
        '助詞': 'Particle',
        '動詞': 'Verb',
        '名詞': 'Noun',
        '形容詞': 'Adjective',
        '形状詞': 'Adjectival noun',
        '感動詞': 'Interjection',
        '接尾辞': 'Suffix',
        '接続詞': 'Conjunction',
        '連体詞': 'Pre-noun adjectival'
    }

    logger.info('Create tokenizer')
    tokenizer_obj: Tokenizer = dictionary.Dictionary().create()

    logger.info('Mode C')
    mode = tokenizer.Tokenizer.SplitMode.C

    logger.info('Create part of speech list by extracting part of speech from word list')
    part_of_speech_list: list[str] = [tokenizer_obj.tokenize(word, mode)[0].part_of_speech()[0] for word in
                                      word_list]

    logger.info('Translate part of speech from Japanese to English and assign to list')
    part_of_speech_list = [jp_pos_tags[part_of_speech] for part_of_speech in part_of_speech_list if
                           part_of_speech in jp_pos_tags]

    return part_of_speech_list


def extract_romanji_from_words(words: list[str]) -> list[str]:
    """
    Extract Romanji from a Japanese word within the list.
    :param words: List of Japanese words String
    :return: List[String]
    """
    return [extract_romanji(word) for word in words]


def extract_romanji(word: str) -> str:
    """
    Extract Romanji from Japanese words.
    :param word: Japanese word String
    :return: Romanji String
    """
    return cutlet.Cutlet().romaji(word)


if __name__ == '__main__':
    pass
