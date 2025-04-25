import json
import os


def load_json_file(file_path: str) -> dict[str, list[dict[str, str]]]:
    """
    Load a single JSON file.
    :param file_path: Path to the JSON file
    :return: JSON data as a dictionary with songs list
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)  # type: ignore


def combine_json_data(json_data_list: list[dict[str, list[dict[str, str]]]]) -> dict[str, list[dict[str, str]]]:
    """
    Combine multiple JSON data dictionaries.
    :param json_data_list: List of JSON data dictionaries
    :return: Combined JSON data as a dictionary
    """
    combined_songs = []
    for data in json_data_list:
        combined_songs.extend(data.get("songs", []))
    return {"songs": combined_songs}


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
    Find all JSON files in the specified directory.

    :param json_dir: Path to the directory containing JSON files.
    :return: List of full paths to JSON files in the directory.
    """
    json_file_path_list = []
    for json_file in os.listdir(json_dir):
        json_file_path_list.append(os.path.join(json_dir, json_file))

    return json_file_path_list
