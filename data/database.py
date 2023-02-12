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

########## User IO ##########

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
            self.users.append(user)
        file.close()

    # Serializes a user to a string. Returns the resulting string.
    def serialize_user(user: User) -> str:
        serialized = user.username + Database.PROPERTY_SEPARATOR + user.password.decode()
        return serialized

    # Deserializes a user from a string. The string should be a serialized user.
    # Returns a User object with the properties from the string.
    def deserialize_user(serialized: str) -> User:
        parts = serialized.split(Database.PROPERTY_SEPARATOR)
        # Users have exactly 2 properties
        if len(parts) != 2:
            Logger.log_error("Serialized user is invalid. Must have exactly 2 string properties - username and password.")
            return None
        # Extract the username and password from the string parts
        username = parts[0]
        password = parts[1].encode("utf-8")
        # Create a user and return it
        user = User(username, password)
        return user

########## Word IO ##########

    # Serializes a word into a string. Returns the resulting string
    def serialize_word(word: Word) -> str:
        serialized = word.term_a + Database.PROPERTY_SEPARATOR\
            + word.term_b + Database.PROPERTY_SEPARATOR\
            + str(word.level) + Database.PROPERTY_SEPARATOR\
            + word.type
        return serialized

    # Deserializes a word from a string. The string should be a serialized word.
    # Returns a Word object with the properties from the string.
    def deserialize_word(serialized: str) -> Word:
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
        word = Word(term_a, term_b, level, type)
        return word

########## Dictionary IO ##########

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
        # Traverse lines of the file
        for line_idx, line in enumerate(file):
            # Handle lines that specify the languages
            if line.startswith(Database.LANGUAGE_A_PREFIX):
                language_a = line[len(Database.LANGUAGE_A_PREFIX):].strip()
                continue
            elif line.startswith(Database.LANGUAGE_B_PREFIX):
                language_b = line[len(Database.LANGUAGE_B_PREFIX):].strip()
                continue
            # At this point the line is a serialized word
            serialized = line.strip()
            word = Database.deserialize_word(serialized)
            if word is None:
                Logger.log_error("Invalid word on line {} of dictionary file {} will be skipped.".format(line_idx + 1, filepath))
                continue
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

    # String used to separate properties of an object when serializing it
    PROPERTY_SEPARATOR = ", "
    # Prefixes of lines in a dictionary file that specify the two languages of the dictionary
    LANGUAGE_A_PREFIX = "__language_a="
    LANGUAGE_B_PREFIX = "__language_b="
    # Default directory for dictionary files
    DEFAULT_DICT_DIRECTORY = "data/dictionaries/"