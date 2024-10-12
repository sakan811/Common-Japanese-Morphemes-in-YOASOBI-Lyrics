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

[![Docker Build](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/docker-build.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/docker-build.yml)

[![Trivy Docker Scan](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/trivy-scan.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/trivy-scan.yml)

# How to Extract Japanese Morphemes from Japanese Song Lyrics
## Setup the Project
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Download [docker-compose.yml](docker-compose.yml) file from this repo.
- Place the Docker Compose file in a directory of your choice.
- Create `lyrics` directory in the same directory that you place the Docker Compose file.

## Add Lyrics as JSON

- Below is a template of the JSON file.
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

### How to Add Songs:
1. Create a new JSON file in the `lyrics` directory.
2. Follow the structure of the JSON file as explained in the above sections.
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

## Setup a Docker Container
- Make sure that Docker Desktop is running.
- Run:
  ```bash
  docker compose up -d
  ```

## Run an App
- Make sure that Dock Desktop and the `morphemes-extractor` container are running.
- Run: 
  ```bash
  docker exec morphemes-extractor python main.py
  ```
- Data is saved to a Postgres database.