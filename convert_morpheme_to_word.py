import asyncio
import glob
import json
import os
import sqlite3
import sys

from loguru import logger

from scraper.data_extractor import extract_data, extract_romanji_from_jp_characters
from scraper.data_transformer import transform_data_to_df
from scraper.web_scraper import get_lyrics_list, return_url_list, async_fetch_page_sources

logger.configure(handlers=[{'sink': sys.stdout, 'level': 'INFO'}])
logger.add('combine_morpheme_to_word.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w', level="INFO")


def combine_morpheme_to_word(morphemes: list[str], dictionary: dict, max_word_length=17):
    """
    Combine morphemes to words by looking at the longest combined morphemes that exist in the dictionary.
    Limit the maximum word length to prevent over-combination.

    :param morphemes: List of morphemes to combine.
    :param dictionary: Japanese dictionary for words lookup.
    :param max_word_length: Maximum allowed length for a combined word.
    :return: List of combined words.
    """
    logger.info("Combining morphemes to words...")
    word_list = []
    pointer1 = 0

    while pointer1 < len(morphemes):
        word_found = False
        # Try the longest possible word starting from pointer1, up to max_word_length
        for pointer2 in range(min(len(morphemes), pointer1 + max_word_length), pointer1, -1):
            word_str = ''.join(morphemes[pointer1:pointer2])
            if word_str in dictionary:
                word_list.append(word_str)
                pointer1 = pointer2
                word_found = True
                break
        if not word_found:
            # If no valid word is found, move pointer 1
            pointer1 += 1

    logger.debug(f"Combined words: {word_list}")
    return word_list


def get_jp_dict() -> dict:
    """
    Create a Japanese dictionary from JSON files from JMDict.
    :return: Japanese dictionary
    """
    logger.info("Creating dictionary from JSON files from JMDict...")
    jmdict_dir = 'jmdict_eng'
    word_dict = {}
    # Find all JSON files in the directory
    json_files = glob.glob(os.path.join(jmdict_dir, '*.json'))
    index_json = os.path.join(jmdict_dir, 'index.json')
    tag_bank_json = os.path.join(jmdict_dir, 'tag_bank_1.json')
    filtered_json_files = [json_file for json_file in json_files if
                           json_file != index_json and json_file != tag_bank_json]
    # Iterate through each JSON file
    for json_file in filtered_json_files:
        # Open and read the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Process each entry in the JSON data
            for entry in data:
                word = entry[0]
                reading = entry[1]
                part_of_speech = entry[2]
                additional_info = entry[3]
                frequency = entry[4]
                meanings = entry[5]
                sequence_number = entry[6]
                tags = entry[7]

                if word not in word_dict:
                    word_dict[word] = []

                word_dict[word].append({
                    "reading": reading,
                    "part_of_speech": part_of_speech,
                    "additional_info": additional_info,
                    "frequency": frequency,
                    "meanings": meanings,
                    "sequence_number": sequence_number,
                    "tags": tags
                })

    return word_dict


def get_pos_from_word(word_list: list[str], jp_dict: dict) -> list[str]:
    """
    Get Part of Speech from words in the list.
    :param word_list: Word list.
    :param jp_dict: Japanese dictionary for words lookup.
    :return: Part of Speech of each word as a list.
    """
    logger.debug('Getting POS tags from dictionary...')
    pos_list = []
    for word in word_list:
        word_data: dict = jp_dict[word][0]
        word_pos = word_data['part_of_speech']
        pos_list.append(word_pos)

    return pos_list


def clean_pos_in_db(database: str) -> None:
    """
    Clean the Part of Speech column in JapaneseWords table.
    :param database: Path to the SQLite database.
    :return: None
    """
    logger.info('Cleaning Part of Speech column...')
    with sqlite3.connect(database) as connection:
        clean_noun_query = '''
        update Word
        set Part_of_Speech = 'Noun'
        where Part_of_Speech glob '[0-9] n*' or Part_of_Speech like 'n%';
        '''
        connection.execute(clean_noun_query)

        clean_verb_query = '''
        update Word
        set Part_of_Speech = 'Verb'
        where Part_of_Speech glob '[0-9] v*' or Part_of_Speech like 'v%';
        '''
        connection.execute(clean_verb_query)

        clean_prt_query = '''
        update Word
        set Part_of_Speech = 'Particle'
        where Part_of_Speech glob '[0-9] prt*' or Part_of_Speech like 'prt%'
        '''
        connection.execute(clean_prt_query)

        clean_adv_query = '''
        update Word
        set Part_of_Speech = 'Adverb'
        where Part_of_Speech glob '[0-9] adv*' or Part_of_Speech like 'adv%'
        '''
        connection.execute(clean_adv_query)

        clean_adj_query = '''
        update Word
        set Part_of_Speech = 'Adjective'
        where Part_of_Speech glob '[0-9] adj*' or Part_of_Speech like 'adj%'
        '''
        connection.execute(clean_adj_query)

        clean_exp_query = '''
        update Word
        set Part_of_Speech = 'Expression'
        where Part_of_Speech glob '[0-9] exp*' or Part_of_Speech like 'exp%'
        '''
        connection.execute(clean_exp_query)

        clean_conj_query = '''
        update Word
        set Part_of_Speech = 'Conjunction'
        where Part_of_Speech glob '[0-9] conj*' or Part_of_Speech like 'conj%'
        '''
        connection.execute(clean_conj_query)

        clean_aux_v_query = '''
        update Word
        set Part_of_Speech = 'Auxiliary Verb'
        where Part_of_Speech glob '[0-9] aux-v*' or Part_of_Speech like 'aux-v%'
                or Part_of_Speech like 'aux%' or Part_of_Speech glob '[0-9] aux*'
        '''
        connection.execute(clean_aux_v_query)

        clean_aux_adj_query = '''
        update Word
        set Part_of_Speech = 'Auxiliary Adjective'
        where Part_of_Speech glob '[0-9] aux-adj*' or Part_of_Speech like 'aux-adj%'
        '''
        connection.execute(clean_aux_adj_query)

        clean_int_query = '''
        update Word
        set Part_of_Speech = 'Interjection'
        where Part_of_Speech glob '[0-9] int*' or Part_of_Speech like 'int%'
        '''
        connection.execute(clean_int_query)

        clean_pronoun_query = '''
        update Word
        set Part_of_Speech = 'Pronoun'
        where Part_of_Speech glob '[0-9] pn*' or Part_of_Speech like 'pn%'
        '''
        connection.execute(clean_pronoun_query)

        clean_copula_query = '''
        update Word
        set Part_of_Speech = 'Copula'
        where Part_of_Speech glob '[0-9] cop*' or Part_of_Speech like 'cop%'
        '''
        connection.execute(clean_copula_query)

        clean_prefix_query = '''
        update Word
        set Part_of_Speech = 'Prefix'
        where Part_of_Speech glob '[0-9] pref*' or Part_of_Speech like 'pref%'
        '''
        connection.execute(clean_prefix_query)

        clean_suffix_query = '''
        update Word
        set Part_of_Speech = 'Suffix'
        where Part_of_Speech glob '[0-9] suf*' or Part_of_Speech like 'suf%'
        '''
        connection.execute(clean_suffix_query)

        clean_counter_query = '''
        update Word
        set Part_of_Speech = 'Counter'
        where Part_of_Speech glob '[0-9] ctr*' or Part_of_Speech like 'ctr%'
        '''
        connection.execute(clean_counter_query)

        clean_unclassifiled_query = '''
        update Word
        set Part_of_Speech = 'Unclassified'
        where Part_of_Speech glob '[0-9] unc*' or Part_of_Speech like 'unc%'
        '''
        connection.execute(clean_unclassifiled_query)

        clean_no_data_query = '''
        update Word
        set Part_of_Speech = 'No POS data'
        where Part_of_Speech like ''
        '''
        connection.execute(clean_no_data_query)


if __name__ == '__main__':
    urls: list[str] = return_url_list()
    page_source_list: list[bytes] = asyncio.run(async_fetch_page_sources(urls))

    db = 'yoasobi.db'

    with sqlite3.connect(db) as connection:
        query = '''
        CREATE TABLE IF NOT EXISTS Word (
            ID INTEGER PRIMARY KEY,
            Word TEXT,
            Romanji TEXT,
            Part_of_Speech TEXT,
            Song TEXT,
            Song_Romanji TEXT,
            Timestamp TIMESTAMP
        );
        '''
        connection.execute(query)
        connection.commit()

    lyrics_lists: list[list[str]] = get_lyrics_list(page_source_list)

    if lyrics_lists:
        jp_dict = get_jp_dict()
        for lyrics_list in lyrics_lists:
            morphemes, romanized_words, part_of_speech_list, song_name = extract_data(lyrics_list)

            word_list: list[str] = combine_morpheme_to_word(morphemes, jp_dict)

            romanji_list: list[str] = extract_romanji_from_jp_characters(word_list)

            pos_list: list[str] = get_pos_from_word(word_list, jp_dict)

            df = transform_data_to_df(word_list, romanji_list, pos_list, song_name, is_morpheme=False)

            df.to_sql('Word', connection, if_exists='append', index=False)

            clean_pos_in_db(db)
    else:
        logger.warning('No lyrics were found. Skipping this page source...')
