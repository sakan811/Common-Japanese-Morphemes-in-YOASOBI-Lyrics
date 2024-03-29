## Common Japanese Words in YOASOBI Lyrics
Update Mar 14th, 2024

Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese words were extracted using **SudachiPy** and romanized using **Cutlet**.

Based on 25 YOASOBI songs

Might not be 100% accurate

This repo only shows codes and raw data

For visualizations, please check out posts below:  
[Instagram](https://www.instagram.com/p/C4f1EjFLNLk/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0yhK1isqssLeCe2TUS8AY9wqtgCEndqK8nzgDfo76MZ67uDa79na7SCKr8f8FHpRRl&id=61553626169836)

## Scripts
```main.py```
- Main script to start all processes.
  - Prompt user whether they want to execute SQL query related to manipulating the table.
    - If the user does not want to execute any of the provided SQL queries, web scraping starts.

## Package ```yoasobi_project```
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