import pytest
from main import Main


def test_main():
    db_dir = 'yoasobi.db'
    Main(db_dir).main()


if __name__ == '__main__':
    pytest.main()
