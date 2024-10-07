import sys

from loguru import logger

from morphemes_extractor.data_extractor import get_morphemes_from_songs
from morphemes_extractor.db_func import save_to_sqlite
from morphemes_extractor.json_utils import find_json_files

logger.configure(handlers=[{'sink': sys.stdout, 'level': 'INFO'}])
logger.add('yoasobi.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w', level="INFO")

db_dir = 'yoasobi.db'

json_dir = 'morphemes_extractor/lyrics'

json_file_path_list = find_json_files(json_dir)

df = get_morphemes_from_songs(json_file_path_list)
save_to_sqlite(df, db_dir)