import sqlite3

import pytest
from main import Main


def test_main():
    db_dir = 'yoasobi.db'
    Main(db_dir).main()

    with sqlite3.connect(db_dir) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Words')
        words = c.fetchall()
        assert len(words) > 0


if __name__ == '__main__':
    pytest.main()
