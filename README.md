## Common Japanese Words in YOASOBI Lyrics
Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese words were extracted using **SudachiPy** and romanized using **Cutlet**.

## Scripts
```main.py```
- Main script to start all processes.
  - Prompt user whether they want to execute SQL query related to manipulating the table.
    - If the user does not want to execute any of the provided SQL queries, web scraping starts.

## Package ```codes```
```extract.py```
- Extract words from the lyrics.

```sql_query.py```
- Return a specific SQL query.

```sqlite_db.py```
- Contain functions that deal with the database itself.

```utils.py```
- Contain utility functions.

```web_scrap.py```
- Scrap lyrics from the given urls.
- Extract song name from the scraped lyrics.
- Return song's lyrics.