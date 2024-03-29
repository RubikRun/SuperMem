from user import User
from logger import Logger
from word import Word
from dictionary import Dictionary
import os

# A class for the database of the application.
# It keeps track of all the data and reads/writes it to text files.
class Database:
    # Creates an empty database
    def __init__(self):
        self.users = []
        self.dictionaries = []
        self.dict_filepaths = []

########## User ##########

    # Exports users to a file
    def export_users(self, filepath: str) -> None:
        file = open(filepath, 'w')
        # Write all the users
        for user in self.users:
            # Serialize each user
            serialized = Database.serialize_user(user)
            # and write it to a line of the file
            file.write(serialized + "\n")
        file.close()

    # Loads users from a file
    def load_users(self, filepath: str) -> None:
        self.users = []
        try:
            file = open(filepath, 'r')
        except FileNotFoundError:
            # If file is not found act as if it's empty
            return
        # Traverse lines of the file
        for line_idx, line in enumerate(file):
            serialized = line.strip()
            user = Database.deserialize_user(serialized)
            if user is None:
                Logger.log_error("Invalid user on line {} of file {} will be skipped.".format(line_idx + 1, filepath))
                continue
            # Set up user's dictionaries.
            self.setup_user_dictionaries(user)
            # Set up user's confidences
            self.setup_user_confidences(user)
            # Add the user to the list
            self.users.append(user)
        file.close()

    # Serializes a user to a string. Returns the resulting string.
    def serialize_user(user: User) -> str:
        # Serialize active languages by connecting them with the elements separator
        if user.active_languages:
            active_languages_serialized = user.active_languages[0]
        else:
            active_languages_serialized = Database.EMPTY_LIST_CHAR
        for language in user.active_languages[1:]:
            active_languages_serialized += Database.ELEMENTS_SEPARATOR + language
        # Serialize active words by connecting them with the elements separator
        if user.active_words:
            active_words_serialized = str(user.active_words[0])
        else:
            active_words_serialized = Database.EMPTY_LIST_CHAR
        for word in user.active_words[1:]:
            active_words_serialized += Database.ELEMENTS_SEPARATOR + str(word)
        # Serialize confidences by connecting them with elements separators
        if user.confidences:
            if user.confidences[0]:
                confidences_serialized = str(user.confidences[0][0])
                for confidence in user.confidences[0][1:]:
                    confidences_serialized += Database.NESTED_ELEMENTS_SEPARATOR + str(confidence)
            else:
                confidences_serialized = Database.NESTED_EMPTY_LIST_CHAR
        else:
            confidences_serialized = Database.EMPTY_LIST_CHAR
        for lang_confidences in user.confidences[1:]:
            confidences_serialized += Database.ELEMENTS_SEPARATOR
            if lang_confidences:
                confidences_serialized += str(lang_confidences[0])
            else:
                confidences_serialized += Database.NESTED_EMPTY_LIST_CHAR
            for confidence in lang_confidences[1:]:
                confidences_serialized += Database.NESTED_ELEMENTS_SEPARATOR + str(confidence)
        # Serialize the user
        serialized = user.username + Database.PROPERTY_SEPARATOR\
            + user.password.decode() + Database.PROPERTY_SEPARATOR\
            + user.main_language + Database.PROPERTY_SEPARATOR\
            + active_languages_serialized + Database.PROPERTY_SEPARATOR\
            + active_words_serialized + Database.PROPERTY_SEPARATOR\
            + confidences_serialized
        return serialized

    # Deserializes a user from a string. The string should be a serialized user.
    # Returns a User object with the properties from the string.
    # NOTE: User's dictionaries are not set up here, because they relate to other parts of the database.
    #       They need to be set up separately.
    def deserialize_user(serialized: str) -> User:
        parts = serialized.split(Database.PROPERTY_SEPARATOR)
        # Users have exactly 6 properties
        if len(parts) != 6:
            Logger.log_error("Serialized user is invalid. Must have exactly 6 properties.")
            return None
        # Extract the properties from the string parts
        username = parts[0]
        password = parts[1].encode("utf-8")
        main_language = parts[2]
        # Handle active languages
        if parts[3] == Database.EMPTY_LIST_CHAR:
            active_languages = []
        else:
            active_languages = [lang.strip() for lang in parts[3].split(Database.ELEMENTS_SEPARATOR)]
        # Handle active words
        if parts[4] == Database.EMPTY_LIST_CHAR:
            active_words = []
        else:
            active_words = [int(words_count) for words_count in parts[4].split(Database.ELEMENTS_SEPARATOR)]
        # Handle confidences
        confidences = []
        if parts[5] != Database.EMPTY_LIST_CHAR:
            for lang_confidence_str in parts[5].split(Database.ELEMENTS_SEPARATOR):
                if lang_confidence_str == Database.NESTED_EMPTY_LIST_CHAR:
                    confidences.append([])
                    continue
                lang_confidences = []
                for confidence_str in lang_confidence_str.split(Database.NESTED_ELEMENTS_SEPARATOR):
                    lang_confidences.append(int(confidence_str))
                confidences.append(lang_confidences)
        # Create a user and return it
        user = User(username, password, main_language, active_languages, active_words, confidences, [])
        return user

    # Finds the dictionaries that user needs for his active languages.
    # For each active language, a dictionary is found between it and the user's main language.
    # User's dictionaries are updated with the found dictionaries
    def setup_user_dictionaries(self, user: User) -> None:
        user.dictionaries = []
        # Traverse active languages, looking for a dictionary for each one
        for language in user.active_languages:
            dict_found = False
            for dictionary in self.dictionaries:
                # We are looking for a dictionary with one of its languages being user's main language
                # and the other being the current active language in the traversal. They can be either (A,B) or (B,A)
                if (dictionary.language_a == user.main_language and dictionary.language_b == language)\
                or (dictionary.language_a == language and dictionary.language_b == user.main_language):
                    user.dictionaries.append(dictionary)
                    dict_found = True
                    break
            # If a dictionary is not found for this active language, this is a problem.
            # Should not happen because if there is no such dictionary then the option of this active language
            # should not have been allowed for the user.
            # If it happens for some reason, log error and append None so that the index matching is kept for the rest of the languages
            if not dict_found:
                Logger.log_error(("A dictionary cannot be found between user's main language ({})"\
                    + " and one of their active languages ({}).").format(user.main_language, language))
                user.dictionaries.append(None)

    # Setup user's confidences.
    # If there are missing confidence values, this function will create them and initialize to 0.
    # If there are more than needed, it will cut the remaining part.
    def setup_user_confidences(self, user: User) -> None:
        languages_count = len(user.active_languages)
        # If there are no confidences, create all of them, fill with 0s
        if not user.confidences:
            user.confidences = []
            for lang_idx in range(languages_count):
                user.confidences.append([0] * user.active_words[lang_idx])
            return
        # If for some of the languages that have confidences, the confidences are fewer than the active words, fill up with 0s
        for lang_idx in range(len(user.confidences)):
            if len(user.confidences[lang_idx]) < user.active_words[lang_idx]:
                user.confidences[lang_idx] += [0] * (user.active_words[lang_idx] - len(user.confidences[lang_idx]))
            elif len(user.confidences[lang_idx]) > user.active_words[lang_idx]:
                user.confidences[lang_idx] = user.confidences[lang_idx][:user.active_words[lang_idx]]
        # If some languages don't have confidences, create and fill with 0s
        if len(user.confidences) < languages_count:
            for lang_idx in range(len(user.confidences), languages_count):
                user.confidences.append([0] * user.active_words[lang_idx])
        elif len(user.confidences) > languages_count:
            user.confidences = user.confidences[:languages_count]

########## Word ##########

    # Serializes a word into a string. Returns the resulting string
    def serialize_word(word: Word) -> str:
        serialized = word.term_a + Database.PROPERTY_SEPARATOR\
            + word.term_b + Database.PROPERTY_SEPARATOR\
            + str(word.level) + Database.PROPERTY_SEPARATOR\
            + word.type
        return serialized

    # Deserializes a word from a string. The string should be a serialized word.
    # Returns a Word object with the properties from the string.
    def deserialize_word(serialized: str, index: int) -> Word:
        parts = serialized.split(Database.PROPERTY_SEPARATOR)
        # Words have exactly 4 properties
        if len(parts) != 4:
            Logger.log_error("Serialized word is invalid. Must have exactly 4 properties.")
            return None
        # Extract the properties from the string parts
        term_a = parts[0]
        term_b = parts[1]
        # Level should be an integer in range [1,100]
        try:
            level = int(parts[2])
        except ValueError:
            Logger.log_error("Serialized word has a non-integer level.")
            return None
        if level < 1 or level > 100:
            Logger.log_error("Serialized word has a level outside of [1,100] range.")
            return None
        # Type should be one of the word types
        type = parts[3]
        if type not in Word.TYPES:
            Logger.log_error("Serialized word has an invalid type.")
            return None
        # Create a word and return it
        word = Word(term_a, term_b, level, type, index)
        return word

########## Dictionary ##########

    # Writes a dictionary to a file
    def write_dictionary(dictionary: Dictionary, filepath: str) -> None:
        file = open(filepath, 'w', encoding = "utf-8")
        # Write the two languages
        file.write(Database.LANGUAGE_A_PREFIX + dictionary.language_a + "\n")
        file.write(Database.LANGUAGE_B_PREFIX + dictionary.language_b + "\n")
        # Write all the words
        for word in dictionary.words:
            # Serialize each word
            serialized = Database.serialize_word(word)
            # and write it to a line of the file
            file.write(serialized + "\n")
        file.close()

    # Reads a dictionary from a file. Returns the dictionary
    def read_dictionary(filepath: str) -> Dictionary:
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested dictionary file does not exist - {}".format(filepath))
            return None
        language_a = None
        language_b = None
        words = []
        word_index = 0
        # Traverse lines of the file
        for line_idx, line in enumerate(file):
            # For now skip empty lines
            # TODO: An empty line should indicate next page, we should keep track of the page of each word
            if len(line) <= 1:
                continue
            # Handle lines that specify the languages
            if line.startswith(Database.LANGUAGE_A_PREFIX):
                language_a = line[len(Database.LANGUAGE_A_PREFIX):].strip()
                continue
            elif line.startswith(Database.LANGUAGE_B_PREFIX):
                language_b = line[len(Database.LANGUAGE_B_PREFIX):].strip()
                continue
            # At this point the line is a serialized word
            serialized = line.strip()
            word = Database.deserialize_word(serialized, word_index)
            if word is None:
                Logger.log_error("Invalid word on line {} of dictionary file {} will be skipped.".format(line_idx + 1, filepath))
                continue
            word_index += 1
            words.append(word)
        file.close()
        # Create a dictionary and return it
        dictionary = Dictionary(language_a, language_b, words)
        return dictionary

    # Exports all the dictionaries in the database to their files
    def export_dictionaries(self):
        if len(self.dictionaries) != len(self.dictionaries):
            Logger.log_error("Different number of dictionaries and filepaths to them.")
            return
        for idx, dictionary in enumerate(self.dictionaries):
            filepath = self.dict_filepaths[idx]
            Database.write_dictionary(dictionary, filepath)

    # Loads dictionaries to the database from text files.
    # If filepaths are not provided, the files from the default dictionary directory will be used
    def load_dictionaries(self, filepaths: list[str] = []):
        if not filepaths:
            filepaths = Database.get_dict_filepaths_from_default_directory()
        self.dictionaries = []
        self.dict_filepaths = filepaths
        # Traverse filepaths
        for filepath in filepaths:
            # Read the dictionary from each file
            dictionary = Database.read_dictionary(filepath)
            # Add it to the database's dictionaries
            self.dictionaries.append(dictionary)

    # Returns a list of paths to the dictionary files in the default dictionary directory
    def get_dict_filepaths_from_default_directory() -> list[str]:
        all_files = os.listdir(Database.DEFAULT_DICT_DIRECTORY)
        txt_files = []
        for file in all_files:
            if file.endswith(".txt"):
                filepath = Database.DEFAULT_DICT_DIRECTORY + file
                txt_files.append(filepath)
        return txt_files

    # Returns a list of all unique languages across the loaded dictionaries
    def get_all_languages(self) -> list[str]:
        languages = []
        for dictionary in self.dictionaries:
            if dictionary.language_a not in languages:
                languages.append(dictionary.language_a)
            if dictionary.language_b not in languages:
                languages.append(dictionary.language_b)
        return languages

    # String used to separate properties of an object when serializing it
    PROPERTY_SEPARATOR = ", "
    # String used to separate elements of properties with multi elements
    ELEMENTS_SEPARATOR = " & "
    NESTED_ELEMENTS_SEPARATOR = "-"
    # Prefixes of lines in a dictionary file that specify the two languages of the dictionary
    LANGUAGE_A_PREFIX = "__language_a="
    LANGUAGE_B_PREFIX = "__language_b="
    # Default directory for dictionary files
    DEFAULT_DICT_DIRECTORY = "data/dictionaries/"
    # A character representing an empty list in a serialized object
    EMPTY_LIST_CHAR = "_"
    NESTED_EMPTY_LIST_CHAR = "."