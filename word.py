from logger import Logger

# A class for a word in two languages.
# "Translation" might be a more descriptive name.
# A word consists of a term in each of the two languages, a level of complexity, and a word type
class Word:
    def __init__(self, term_a: str, term_b: str, level: int, type: str, index: int):
        self.term_a = term_a
        self.term_b = term_b
        self.level = level
        if type in Word.TYPES:
            self.type = type
        else:
            Logger.log_error("Trying to create a word with invalid type - {}. It will be created with default type.".format(type))
            self.type = Word.DEFAULT_TYPE
        self.index = index

    TYPES = ["noun", "verb", "adj", "pron", "prepos", "conj", "interj", "expr", "unknown"]
    DEFAULT_TYPE = "noun"