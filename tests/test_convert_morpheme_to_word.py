import sqlite3

from convert_morpheme_to_word import convert_morpheme_to_word_main


def test_convert_morpheme_to_word():
    db = 'test_convert_morpheme_to_word.db'
    html = 'tests/yoasobi_undead_lyrics.html'

    convert_morpheme_to_word_main(db, is_test=True, test_html=html)

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Word')
        results = cur.fetchall()
        assert results != []

