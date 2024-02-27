## Common Japanese Words in YOASOBI Lyrics
Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese words were extracted using **SudachiPy** and romanized using **Cutlet**.

Based on 25 YOASOBI songs

Might not be 100% accurate

This repo only shows codes and raw data

For visualizations, please check out my Facebook page's post:
https://www.facebook.com/permalink.php?story_fbid=pfbid0tUMSFW8r6i9xk4S46miEaertmGk4jexSEMMRiWdbvAwQAKodqMPC2GHb2R38uT8cl&id=61553626169836

## Scripts
```main.py```
- Main script to start all processes.
  - Prompt user whether they want to execute SQL query related to manipulating the table.
    - If the user does not want to execute any of the provided SQL queries, web scraping starts.

## Package ```yoasobi_project_package```
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