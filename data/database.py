from user import User
from logger import Logger

# A class for the database of the application.
# It keeps track of all the data and reads/writes it to text files.
class Database:
    # Creates an empty database
    def __init__(self):
        self.users = []

    # Reads users from a file
    def read_users(self, filepath: str) -> None:
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
        
    # Writes users to a file
    def write_users(self, filepath: str) -> None:
        file = open(filepath, 'w')

        for user in self.users:
            # Serialize each user
            serialized = Database.serialize_user(user)
            # and write it to a line of the file
            file.write(serialized + "\n")

        file.close()

    # Serializes a user. Merges all its properties into a single string that can be written to a text file.
    # Returns the resulting string.
    def serialize_user(user: User) -> str:
        serialized = user.username + Database.PROPERTY_SEPARATOR + user.password.decode()
        return serialized

    # Deserializes a user. Extracts all its properties from the given string, which is a serialized user.
    # Returns a user object with the properties from the string.
    def deserialize_user(serialized: str) -> User:
        parts = serialized.split(Database.PROPERTY_SEPARATOR)
        # Users have exactly 2 properties
        if len(parts) != 2:
            Logger.log_error("Serialized user is invalid. Must have exactly 2 string properties - username and password")
            return None
        # Extract the username and password from the string parts
        username = parts[0]
        password = parts[1].encode("utf-8")
        # Create a user and return it
        user = User(username, password)
        return user

    # String used to separate properties of an object when serializing it
    PROPERTY_SEPARATOR = ", "