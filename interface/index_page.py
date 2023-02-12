from interface.cli import CLI
from interface.login_page import LoginPage
from interface.register_page import RegisterPage
from user import User
from typing import List

# A class for a CLI index page.
# It's the first thing that opens when you start the application.
# It lets you login or register.
class IndexPage:
    # Runs the index page.
    # Expects a list of registered users, as a parameter.
    def run(users: List[User]) -> None:
        while True:
            CLI.print_big("Welcome to SuperMem!")
            CLI.print("Choose an option, or type \"exit\":\n")
            CLI.print("1. Login\n")
            CLI.print("2. Register\n")

            option = CLI.ask_option([1, 2])

            if option == 1:
                user = LoginPage.run(users)
            else:
                user = RegisterPage.run()
                users.append(user)
                