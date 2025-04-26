import json
import os
import pathlib

SONGS_KEY = "songs"


def load_json_file(file_path: str) -> dict[str, list[dict[str, str]]]:
    """
    Load a single JSON file securely.
    :param file_path: Path to the JSON file
    :return: JSON data as a dictionary with songs list
    """
    # Only allow .json files in the lyrics directory
    base_dir = pathlib.Path(__file__).parent.parent / 'lyrics'
    abs_path = pathlib.Path(file_path).resolve()
    if not abs_path.is_file() or abs_path.suffix != '.json' or base_dir not in abs_path.parents:
        raise ValueError(f"Invalid or unauthorized file path: {file_path}")
    with open(abs_path, 'r', encoding='utf-8') as file:
        return json.load(file)  # type: ignore


def combine_json_data(json_data_list: list[dict[str, list[dict[str, str]]]]) -> dict[str, list[dict[str, str]]]:
    """
    Combine multiple JSON data dictionaries.
    :param json_data_list: List of JSON data dictionaries
    :return: Combined JSON data as a dictionary
    """
    combined_songs = []
    for data in json_data_list:
        combined_songs.extend(data.get(SONGS_KEY, []))
    return {SONGS_KEY: combined_songs}


def load_json(json_file_path_list: list[str]) -> dict[str, list[dict[str, str]]]:
    """
    Load JSON data from multiple files and combine them.
    :param json_file_path_list: List of paths to JSON files
    :return: Combined JSON data as a dictionary
    """
    json_data_list = [load_json_file(file_path) for file_path in json_file_path_list]
    return combine_json_data(json_data_list)


def find_json_files(json_dir: str) -> list[str]:
    """
    Find all JSON files in the specified directory securely.
    :param json_dir: Path to the directory containing JSON files.
    :return: List of full paths to JSON files in the directory.
    """
    base_dir = pathlib.Path(__file__).parent.parent / 'lyrics'
    abs_dir = pathlib.Path(json_dir).resolve()
    # Ensure the resolved path is strictly within the base directory
    if not abs_dir.is_dir() or os.path.commonpath([base_dir, abs_dir]) != str(base_dir):
        raise ValueError(f"Invalid or unauthorized directory: {json_dir}")
    json_file_path_list = []
    for json_file in os.listdir(abs_dir):
        if json_file.endswith('.json'):
            file_path = abs_dir / json_file
            if file_path.is_file():
                json_file_path_list.append(str(file_path))
    return json_file_path_list
