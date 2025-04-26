# Common Japanese Morphemes in YOASOBI Lyrics

Showcase **visualizations** about the common **Japanese morphemes** in **YOASOBI**'s songs' lyrics.

> Morphemes are the smallest units of meaning in a language.

- Japanese morphemes were extracted using **SudachiPy** and romanized using **Cutlet**.

## Disclaimers

- Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)
- Lyrics of 29 YOASOBI songs

## Visualizations

[Click here](./docs/VISUALS.md) to see the visualizations.

## Status

[![Python Test](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/python-test.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/python-test.yml)

[![Docker CI](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics/actions/workflows/docker-ci.yml)

## Call APIs to Extract Japanese Morphemes from YOASOBI's Song Lyrics

### Prerequisites

- Install UV: <https://docs.astral.sh/uv/getting-started/installation/>
- Install Docker Desktop: <https://www.docker.com/products/docker-desktop/>

### Setup the Project

- Clone the repository:

  ```bash
  git clone https://github.com/sakan811/Common-Japanese-Morphemes-in-YOASOBI-Lyrics.git 
  ```

- Setup .env file:

  ```bash
  cp .env.example .env
  ```

- Setup Docker Container:

  ```bash
  docker compose up -d
  ```

### Add Lyrics as JSON

- Below is a [JSON template file](./lyrics/template.json) in [lyrics](./lyrics/) directory.

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

#### Explanation

- The JSON file contains an array of `songs`.
- Each song in the array has three fields:
  - `title`: The original Japanese title of the song.
  - `romanji_title`: The romanized version of the title.
  - `lyrics`: The full lyrics of the song in Japanese.

#### How to Add Songs

1. Create a new JSON file in the `lyrics` directory.
2. Follow the structure of the JSON file as explained in the above sections.
3. For each new song, add a new object to the `songs` array with the required fields.
4. Make sure to separate multiple song objects with commas.
5. Save the file with a meaningful name (e.g., `yoasobi_songs.json`).
6. The script will automatically process all JSON files in the lyrics directory.

> You can seperate songs into its own JSON file, but the JSON structure should be as instructed

#### Example of adding multiple songs

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

### Call the APIs

- Call the API that extracts morphemes from the lyrics:

  ```bash
  curl -X POST "http://localhost:8000/extract-morphemes/" \
    -H "Content-Type: application/json" \
    -d "{\"json_dir\": \"lyrics\"}"
  ```

  - Data is saved to a Docker Postgres database.

- Call the API that creates visualizations:

  ```bash
  curl -X POST "http://localhost:8000/visualize/" \
    -H "Content-Type: application/json" \
    -d '{"font_scale": 2.0}'
  ```

  - The visualizations will be saved to the `visual_output` directory
