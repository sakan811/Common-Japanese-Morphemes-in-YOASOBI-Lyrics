## Common Japanese Words in YOASOBI Lyrics
Update May 4th, 2024

Showcase visualizations about the common Japanese words in YOASOBI's songs' lyrics.

## Project Details
Lyrics were based on [genius.com](https://genius.com/artists/Yoasobi)

Japanese words were extracted using **SudachiPy** and romanized using **Cutlet**.

Based on 25 YOASOBI songs

Might not be 100% accurate

## Visualizations
[Instagram](https://www.instagram.com/p/C6i6BEoLKJO/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0xonwCJKm8aDZEM3BAQonTGVLfU6SEoKhKWFvBuGRAwLdCSnGbJsBmrq55p22fDcYl&id=61553626169836)

## Code Base Details
### To Start Web-scraping Process
- Go to ```main.py```
- Run the script.
- SQLite database 'yoasobi.db' will be initialized.

### Package ```yoasobi_project```
```extract.py```
- Extract words from the lyrics.

```sql_query.py```
- Return a specific SQL query.

```sqlite_db.py```
- Contain functions that deal with the database itself.
- Migrate the scraped data to SQLite database.

```utils.py```
- Contain utility functions.

```web_scrap.py```
- Scrap lyrics from the given urls.
- Extract song name from the scraped lyrics.
- Return song's lyrics.

### Test result
[test_result.html](test_result.html)
- This HTML stores the test result of this code base that I ran locally.
  - I can't use GitHub Action pipeline to test as Genius.com seems to block GitHub Action's IP address,
  making the script failed to fetch the desired HTML content.
