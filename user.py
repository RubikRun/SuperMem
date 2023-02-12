MIN_USERNAME_LEN = 3
MIN_PASSWORD_LEN = 6
USERNAME_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
PASSWORD_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# A class for a user of the application
class User:
    # Creates a user with a username, password, their main language and their active languages
    def __init__(self, username: str, password: bytes, main_language: str, active_languages: list[str] = []):
        self.username = username
        self.password = password
        self.main_language = main_language
        self.active_languages = active_languages

    # Checks if a username is valid
    def is_username_valid(username: str) -> bool:
        if username is None or len(username) < MIN_USERNAME_LEN:
            return False
        for char in username:
            if char not in USERNAME_ALLOWED_CHARS:
                return False
        return True

    # Checks if a password is valid
    def is_password_valid(password: str) -> bool:
        if password is None or len(password) < MIN_PASSWORD_LEN:
            return False
        for char in password:
            if char not in PASSWORD_ALLOWED_CHARS:
                return False
        return True

    VALID_USERNAME_MSG = "Username should be at least " + str(MIN_USERNAME_LEN) + " characters"\
    + " and contain only letters A-Z, a-z and numbers."
    VALID_PASSWORD_MSG = "Password should be at least " + str(MIN_PASSWORD_LEN) + " characters"\
    + " and contain only letters A-Z, a-z and numbers."