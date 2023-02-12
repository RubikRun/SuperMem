from interface.cli import CLI
from user import User
import bcrypt

MIN_USERNAME_LEN = 3
MIN_PASSWORD_LEN = 6
USERNAME_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
PASSWORD_ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# A class for a CLI page for user registration
class RegisterPage:
    # Runs the user registration page. Returns the registrated user.
    def run() -> User:
        # Ask for username and password
        username = RegisterPage.ask_username()
        password = RegisterPage.ask_password()
        # Create the user and return it
        user = User(username, password)
        return user

    # Checks if a user input is valid with some minimum length and allowed characters
    def is_input_valid(input: str, min_len: int, allowed_chars: str) -> bool:
        if input is None or len(input) < min_len:
            return False
        for char in input:
            if char not in allowed_chars:
                return False
        return True

    # Asks user to choose a username, until they choose a valid one. Returns the username.
    def ask_username() -> str:
        username = username = CLI.ask_for("Choose a username: ")
        # Until the entered username is invalid, keep asking
        while not RegisterPage.is_input_valid(username, MIN_USERNAME_LEN, USERNAME_ALLOWED_CHARS):
            CLI.print("Invalid username. Should be at least " + str(MIN_USERNAME_LEN) + " characters"
            " and contain only letters A-Z, a-z and numbers.\n")
            username = CLI.ask_for("Choose a username: ")
        # Return the valid username
        return username

    # Asks user to choose a password, until they choose a valid one. Returns the password hashed.
    def ask_password() -> str:
        password = CLI.ask_password("Choose a password: ")
        # Until the password is invalid, keep asking
        while not RegisterPage.is_input_valid(password, MIN_PASSWORD_LEN, PASSWORD_ALLOWED_CHARS):
            CLI.print("Invalid password. Should be at least " + str(MIN_PASSWORD_LEN) + " characters"
            " and contain only letters A-Z, a-z and numbers.\n")
            password = CLI.ask_password("Choose a password: ")
        # Hash the valid password and return it
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash
        
