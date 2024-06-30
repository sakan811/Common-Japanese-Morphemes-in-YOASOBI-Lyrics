## Common Japanese Morphemes in YOASOBI Lyrics
Latest Update: 30 June 2024

Showcase visualizations about the common Japanese morphemes in YOASOBI's songs' lyrics.

Morphemes are the smallest units of meaning in a language.

## Status
[![CodeQL](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/codeql.yml)    
[![Scraper Test](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml/badge.svg)](https://github.com/sakan811/Common-Japanese-Words-in-YOASOBI-Lyrics/actions/workflows/scraper-test.yml)

## Project Details
Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese morphemes were extracted using **SudachiPy** and romanized using **Cutlet**.

Based on 26 YOASOBI songs

## Visualizations
[Power BI](https://app.powerbi.com/view?r=eyJrIjoiMTljZjdmN2MtMTk2NC00N2M5LTkxNGMtN2NhZDhlNmU4YmUzIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)    
[Instagram](https://www.instagram.com/p/C79n7lEhY-O/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/photo/?fbid=122156667290120872&set=pcb.122156667518120872)

## Code Base Details
### To Start Web-scraping Process
- Go to ```main.py```
- Run the script.
- Data is saved to a SQLite database 'yoasobi.db'.
  - The database will be created automatically if not exist. 

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


