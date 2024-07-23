import asyncio
import datetime
import glob
import json
import os
import sqlite3
import sys
import pandas as pd
from loguru import logger

from yoasobi_pipeline.pipeline import get_all_page_source
from yoasobi_pipeline.yoasobi_scraper.data_extractor import extract_data, extract_romanji_from_jp_characters, \
    extract_romanji
from yoasobi_pipeline.yoasobi_scraper.web_scraper import get_lyrics_list

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


if __name__ == '__main__':
    page_source_list = asyncio.run(get_all_page_source())

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

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            data_dict = {
                'word': word_list,
                'romanji': romanji_list,
                'part_of_speech': pos_list
            }

            df = pd.DataFrame(data=data_dict)

            df['song'] = song_name
            df['song_romanji'] = extract_romanji(song_name)
            df['timestamp'] = timestamp

            df.to_sql('Word', connection, if_exists='append', index=False)
    else:
        logger.warning('No lyrics were found. Skipping this page source...')
