from word import Word
from typing import List

# A class for a dictionary of words between two languages.
class Dictionary:
    def __init__(self, language_a: str, language_b: str, words: List[Word]):
        self.language_a = language_a
        self.language_b = language_b
        self.words = words