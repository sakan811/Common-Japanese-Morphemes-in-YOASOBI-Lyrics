# Table of Contents
- [Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics)
- [Common Japanese Words in YOASOBI Lyrics](#common-japanese-words-in-yoasobi-lyrics)
- [Codebase Details](#codebase-details)

# Updates
[Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics):

- Project Latest Update: 24 July 2024

[Common Japanese Words in YOASOBI Lyrics](#common-japanese-words-in-yoasobi-lyrics):

- Project Latest Update: 24 July 2024

# Disclaimers
- Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)
- Lyrics of 26 YOASOBI songs

# Visualizations
[Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics):
- Visualizations Latest Update: 24 July 2024
  - [Power BI](https://app.powerbi.com/view?r=eyJrIjoiMTljZjdmN2MtMTk2NC00N2M5LTkxNGMtN2NhZDhlNmU4YmUzIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)
  - [Instagram](https://www.instagram.com/p/C90Am-KhCsX/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)
  - [Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid02X9XERHLkiGgnKFdBPhapgpx2EgR6HzXand9BbqmsKjQwC5w7hqxrwu3YELRxLLBAl&id=61553626169836)

[Common Japanese Words in YOASOBI Lyrics](#common-japanese-words-in-yoasobi-lyrics):
- Visualizations Latest Update: 24 July 2024
  - [Power BI](https://app.powerbi.com/view?r=eyJrIjoiODk0NDIyMjYtODQ2YS00NDgzLWI4MDctNjA4ZTQ1MTdkZTNlIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)
  - [Instagram](https://www.instagram.com/p/C90NslNBNrl/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)
  - [Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid026e9oDZTyynRPeixJFjkAQ4sdCKwUytqB14ELyLexGJ6hz4oZvaz43y1KQU1pyUBEl&id=61553626169836)

# Common Japanese Morphemes in YOASOBI Lyrics
Showcase visualizations about the common Japanese morphemes in YOASOBI's songs' lyrics.

Morphemes are the smallest units of meaning in a language.

## Project Details
Japanese morphemes were extracted using **SudachiPy** and romanized using **Cutlet**.


# Common Japanese Words in YOASOBI Lyrics
Showcase visualizations about the common Japanese words in YOASOBI's songs' lyrics.

This project is built on top of [Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics) project.


## Project Details
Find the Japanese words by combining morphemes into words by looking up at the dictionary.

Japanese morphemes were extracted using **SudachiPy** and romanized using **Cutlet**.

[JMdict](https://github.com/themoeway/jmdict-yomitan) was used for words look-up.


# Codebase Details
[Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics) and
[Common Japanese Words in YOASOBI Lyrics](#common-japanese-words-in-yoasobi-lyrics) projects share the same codebase.


## Test Status
[![CodeQL](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml) 

[![Scraper Test](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml)

## To Scrape Japanese Morphemes from YOASOBI's Songs
- Go to [main.py](main.py)
- Run the script.
- Data is saved to a SQLite database named **yoasobi.db** by default.
  - The database is created automatically if not exist in the given path. 
  - You can adjust the name of the database as defined in [main.py](main.py)
    ```
    db_dir = 'yoasobi.db'  # adjust this variable to change the database's name
    ```

## To Scrape Japanese Words from YOASOBI's Songs
- Go to [convert_morpheme_to_word.py](convert_morpheme_to_word.py)
- Run the script.
- Data is saved to a SQLite database named **yoasobi.db** by default.
  - The database is created automatically if not exist in the given path. 
  - You can adjust the name of the database as defined in [convert_morpheme_to_word.py](convert_morpheme_to_word.py)
    ```
    db = 'yoasobi.db'  # adjust this variable to change the database's name
    ```

## [scraper](scraper) Package 
[data_extractor.py](scraper%2Fdata_extractor.py)
- Contain functions related to extracting the desired data.

[data_transformer.py](scraper%2Fdata_transformer.py)
- Contain functions to transform the data.

[sql_query.py](scraper%2Fsql_query.py)
- Return a specific SQL query.

[utils.py](scraper%2Futils.py)
- Contain utility functions.

[web_scraper.py](scraper%2Fweb_scraper.py)
- Contain functions related to fetching content from the webpage.

[db_func.py](scraper%2Fdb_func.py)
- Contain functions to related to the database.