from interface.cli import CLI
from interface.login_page import LoginPage
from interface.register_page import RegisterPage
from interface.home_page import HomePage
from user import User
from data.database import Database

# A class for a CLI index page.
# It's the first thing that opens when you start the application.
# It lets you login or register.
class IndexPage:
    # Runs the index page.
    # Expects a list of registered users, as a parameter.
    def run(users: list[User], database: Database) -> None:
        while True:
            # Print welcome message and ask user to choose login or register
            CLI.print_big("Welcome to SuperMem!")
            option = CLI.ask_option_num(
                "Choose an option, or type \"exit\":", [
                "Login",
                "Register"
            ])
            # If option is None we need to exit
            if option is None:
                return
            # Redirect to login or register page based on the chosen option
            elif option == 1:
                user = LoginPage.run(users)
                home_page = HomePage(user)
                home_page.run(database)
                # After exiting the home page user is back to the index page
            else:
                # Register a user and add it to the list of users
                user = RegisterPage.run(database.get_all_languages())
                users.append(user)
                # After registration user is back to the index page so that they can login
                