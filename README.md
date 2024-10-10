# Common Japanese Morphemes in YOASOBI Lyrics
Showcase visualizations about the common Japanese morphemes in YOASOBI's songs' lyrics.

> Morphemes are the smallest units of meaning in a language.

- Japanese morphemes were extracted using **SudachiPy** and romanized using **Cutlet**.

# Disclaimers
- Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)
- Lyrics of 28 YOASOBI songs

# Visualizations
[Common Japanese Morphemes in YOASOBI Lyrics](#common-japanese-morphemes-in-yoasobi-lyrics):
- Visualizations Latest Update: 8 October 2024
  - [Power BI](https://app.powerbi.com/view?r=eyJrIjoiMTljZjdmN2MtMTk2NC00N2M5LTkxNGMtN2NhZDhlNmU4YmUzIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)
  - [Instagram](https://www.instagram.com/p/DA3StTcNmo0/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)
  - [Facebook](https://www.facebook.com/share/p/Do5gMdTYYpmgvc52/)

# Status
[![CodeQL](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml) 

[![Python Test](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/python-test.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/python-test.yml)

# How to Extract Japanese Morphemes from YOASOBI's Song Lyrics
## Setup the Project
- Clone this repo: https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics.git
- Install the dependencies: 
  * ```bash
    pip install -r requirements.txt 
    ```
- Download Unidic:
  - ```bash
    python -m unidic download
    ``` 

## Add Lyrics as JSON

- [template.json](morphemes_extractor%2Flyrics%2Ftemplate.json) is a template of the JSON file.
  ```json
  {
    "songs": [
      {
        "title": "",
        "romanji_title": "",
        "lyrics": ""
      }
    ]
  }
  ```

### Explanation:
- The JSON file contains an array of `songs`.
- Each song in the array has three fields:
  - `title`: The original Japanese title of the song.
  - `romanji_title`: The romanized version of the title.
  - `lyrics`: The full lyrics of the song in Japanese.

### How to Add More Songs:
1. Create a new JSON file in the `morphemes_extractor/lyrics` directory or use an existing one.
2. Follow the structure of the [template.json](morphemes_extractor%2Flyrics%2Ftemplate.json) file.
3. For each new song, add a new object to the `songs` array with the required fields.
4. Make sure to separate multiple song objects with commas.
5. Save the file with a meaningful name (e.g., `yoasobi_songs.json`).
6. The script will automatically process all JSON files in the lyrics directory.
### Example of adding multiple songs:
```json
{
  "songs": [
    {
      "title": "夜に駆ける",
      "romanji_title": "Yoru ni Kakeru",
      "lyrics": "ふざけあっても 分かり合えた気がした..."
    },
    {
      "title": "群青",
      "romanji_title": "Gunjou",
      "lyrics": "嗚呼いつもの様に 過ぎる日々にあくびが出る..."
    }
  ]
}
```

## Run a Script
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