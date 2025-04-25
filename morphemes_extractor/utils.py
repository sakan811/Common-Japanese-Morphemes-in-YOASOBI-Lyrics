import logging
from morphemes_extractor.jp_data import MorphemeData
from morphemes_extractor.logger_config import setup_logger

# Set up logger
logger: logging.Logger = setup_logger(__name__, logging.INFO)


def check_list_len(morpheme_data: MorphemeData) -> tuple[int, ...]:
    """
    Calculate the length of the target list and return it as an integer.
    :param morpheme_data: MorphemeData object containing target lists.
    :return: Length of the target list as Tuple.
    """
    logger.info("Checking length of target lists...")
    lengths = [
        len(morpheme_data.morphemes),
        len(morpheme_data.romanized_morphemes),
        len(morpheme_data.part_of_speech_list),
    ]
    logger.debug(f"Lengths: {lengths}")
    return tuple(lengths)


if __name__ == "__main__":
    pass
