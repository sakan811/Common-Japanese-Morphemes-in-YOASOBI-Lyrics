import sqlite3

from main import start_scraper


def test_main():
    db = 'test_main.db'
    html = 'tests/yoasobi_undead_lyrics.html'

    start_scraper(db, is_test=True, test_html=html)

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Morpheme')
        results = cur.fetchall()
        assert results != []
