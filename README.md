## Common Japanese Words in YOASOBI Lyrics
Update May 25th, 2024

Showcase visualizations about the common Japanese words in YOASOBI's songs' lyrics.

## Status
[![CodeQL](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml)  
[![Python application](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/python-app.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/python-app.yml)

## Project Details
Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese words were extracted using **SudachiPy** and romanized using **Cutlet**.

Based on 25 YOASOBI songs

## Visualizations
[Instagram](https://www.instagram.com/p/C7ZeZaath92/?img_index=1)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid022KbDh4a2yewBPKe6hySvzpSSWUvaB9ZWDsnXnWctASUqucLxiFFtN1PrjU5snSn3l&id=61553626169836)

## Code Base Details
### To Start Web-scraping Process
- Go to ```yoasobiscraper.py```
- Run the script.
- SQLite database 'yoasobi.db' will be initialized.

### [yoasobi_pipeline](yoasobi_pipeline) Package 
```pipeline.py```
- Contain functions of the web-scraping pipeline.

### [yoasobi_scraper](yoasobi_pipeline%2Fyoasobi_scraper) Package
```data_extractor.py```
- Contain functions related to extracting the desired data.

```sql_query.py```
- Return a specific SQL query.

```sqlite_db.py```
- Contain functions that deal with the database itself.
- Migrate the scraped data to SQLite database.

```utils.py```
- Contain utility functions.

```web_scraper.py```
- Contain functions related to fetching content from the webpage.


