from interface.cli import CLI
from user import User
import bcrypt

# A class for a CLI page for user registration
class RegisterPage:
    # Runs the user registration page. Returns the registrated user.
    def run(languages: list[str]) -> User:
        CLI.print_big("Register to SuperMem")
        # Ask for username and password
        username = RegisterPage.ask_username()
        password = RegisterPage.ask_password()
        main_language = CLI.ask_option("What's your main language?", languages)
        # Create the user and return it
        user = User(username, password, main_language, [], [], [], [])
        CLI.print("User {} created successfully.".format(username))
        return user

    # Asks user to choose a username, until they choose a valid one. Returns the username.
    def ask_username() -> str:
        username = CLI.ask_for("Choose a username: ")
        # Until the entered username is invalid, keep asking
        while not User.is_username_valid(username):
            CLI.print("Invalid username. " + User.VALID_USERNAME_MSG + "\n")
            username = CLI.ask_for("Choose a username: ")
        # Return the valid username
        return username

    # Asks user to choose a password, until they choose a valid one. Returns the password hashed.
    def ask_password() -> str:
        password = CLI.ask_password("Choose a password: ")
        # Until the password is invalid, keep asking
        while not User.is_password_valid(password):
            CLI.print("Invalid password. " + User.VALID_PASSWORD_MSG + "\n")
            password = CLI.ask_password("Choose a password: ")
        # Hash the valid password and return it
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash
        
