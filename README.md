# Common Japanese Morphemes in YOASOBI Lyrics
Showcase visualizations about the common Japanese morphemes in YOASOBI's songs' lyrics.

> Morphemes are the smallest units of meaning in a language.

- Project Latest Update: 24 July 2024
- Japanese morphemes were extracted using **SudachiPy** and romanized using **Cutlet**.

# Disclaimers
- Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)
- Lyrics of 28 YOASOBI songs

# Visualizations
[Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics):
- Visualizations Latest Update: 6 October 2024
  - [Power BI](https://app.powerbi.com/view?r=eyJrIjoiMTljZjdmN2MtMTk2NC00N2M5LTkxNGMtN2NhZDhlNmU4YmUzIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)
  - [Instagram]()
  - [Facebook]()

# Status
[![CodeQL](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml) 

[![Scraper Test](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml)

# How to Scrape Japanese Morphemes from YOASOBI's Songs
## Setup the Project
- Clone this repo: https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics.git

## Run the Script
- Run:
  ```bash
  python main.py
  ```
> Data is saved to a SQLite database named **yoasobi.db** by default.
>  - The database is created automatically if not exist in the given path. 
> - You can adjust the name of the database as defined in [main.py](main.py)
>  ```
>  db_dir = 'yoasobi.db'  # adjust this variable to change the database's name
>  ```