from dataclasses import dataclass
from typing import List


@dataclass
class MorphemeData:
    morphemes: List[str]
    romanized_morphemes: List[str]
    part_of_speech_list: List[str]
