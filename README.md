## Common Japanese Words in YOASOBI Lyrics
Update June 4th, 2024

Showcase visualizations about the common Japanese words in YOASOBI's songs' lyrics.

## Status
[![CodeQL](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml)    
[![Scraper Test](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml)

## Project Details
Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese words were extracted using **SudachiPy** and romanized using **Cutlet**.

Based on 25 YOASOBI songs

## Visualizations
[Power BI](https://app.powerbi.com/view?r=eyJrIjoiMTljZjdmN2MtMTk2NC00N2M5LTkxNGMtN2NhZDhlNmU4YmUzIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)    
[Instagram](https://www.instagram.com/p/C7y-gtDvp4J/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0Bcsp77fccLUMsjLxg34B8UyGCh8zgHHSmRaqzed1tKyrjPwVFCxxYXddieF8Z9q5l&id=61553626169836)

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


