from interface.cli import CLI
from user import User
import bcrypt

# A class for a CLI page for user login
class LoginPage:
    # Runs the user login page. Returns the logged in user.
    # Expects a list of registered users, as a parameter.
    def run(users: list[User]) -> User:
        CLI.print_big("Login to SuperMem")
        while True:
            # Ask for username and password
            username = LoginPage.ask_username()
            password = LoginPage.ask_password()
            # Get the user with the entered data from all the users
            user = LoginPage.get_user(users, username, password)
            # If found, return it, otherwise print message and repeat
            if user is None:
                CLI.print("Wrong username or password. Try again.\n")
            else:
                return user

    # Finds the user with the given username, checks if the given password matches. Returns the user.
    def get_user(users: list[User], username: str, password: str) -> User:
        bytes = password.encode("utf-8")
        for user in users:
            # If username matches, this is surely the user, because usernames are unique
            if username == user.username:
                # If password matches, everything good - return the user
                if bcrypt.checkpw(bytes, user.password):
                    return user
                # otherwise wrong password - stop looking for user
                else:
                    break
        # If user not found, or wrong password entered, return None
        return None

    # Asks user for their username.
    def ask_username() -> str:
        username = CLI.ask_for("Username: ")
        return username

    # Asks user for their password.
    def ask_password() -> str:
        password = CLI.ask_password("Password: ")
        return password