from interface.cli import CLI
from user import User
from typing import List
import bcrypt

# A class for a CLI page for user login
class LoginPage:
    # Runs the user login page. Returns the logged in user.
    # Expects a list of registered users, as a parameter.
    def run(users: List[User]) -> User:
        CLI.print_big("Login to SuperMem")
        while True:
            username = LoginPage.ask_username()
            password = LoginPage.ask_password()
            user = LoginPage.get_user(users, username, password)
            if user is None:
                CLI.print("Wrong username or password. Try again.\n")
            else:
                return user

    # Finds the user with the given username, checks if the given password matches. Returns the user.
    def get_user(users: List[User], username: str, password: str) -> User:
        bytes = password.encode("utf-8")
        for user in users:
            if username == user.username:
                if bcrypt.checkpw(bytes, user.password):
                    return user
                else:
                    break
        return None

    # Asks user for their username.
    def ask_username() -> str:
        username = username = CLI.ask_for("Username: ")
        return username

    # Asks user for their password.
    def ask_password() -> str:
        password = CLI.ask_password("Password: ")
        return password