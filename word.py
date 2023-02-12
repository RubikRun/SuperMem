# A class for a word in two languages.
# "Translation" might be a more descriptive name.
# A word consists of a term in each of the two languages, a level of complexity, and a word type
class Word:
    def __init__(self, term_a: str, term_b: str, level: int, type: int):
        self.term_a = term_a
        self.term_b = term_b
        self.level = level
        self.type = type

    WORD_TYPES = ["noun", "verb", "adjective", "pronoun", "preposition", "conjuction", "interjection", "expression"]