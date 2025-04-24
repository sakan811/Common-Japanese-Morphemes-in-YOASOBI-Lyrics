import os
import sys

from loguru import logger

from morphemes_extractor.data_extractor import get_morphemes_from_songs
from morphemes_extractor.db_func import save_to_db
from morphemes_extractor.json_utils import find_json_files

logger.add(sys.stderr, level="WARNING")


def main(db_url: str, json_dir: str) -> None:
    json_file_path_list = find_json_files(json_dir)
    if json_file_path_list:
        df = get_morphemes_from_songs(json_file_path_list)
        if not df.empty:
            save_to_db(df, db_url)
        else:
            logger.warning("No morphemes found in the JSON files.")
    else:
        logger.warning("No JSON files found in the specified directory.")


if __name__ == '__main__':
    json_dir = os.getenv('JSON_DIR')
    if json_dir is None:
        logger.error("JSON_DIR environment variable is not set.")
        sys.exit(1)

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    main(db_url, json_dir)