from interface.cli import CLI
from interface.login_page import LoginPage
from interface.register_page import RegisterPage
from user import User

# A class for a CLI index page.
# It's the first thing that opens when you start the application.
# It lets you login or register.
class IndexPage:
    # Runs the index page.
    # Expects a list of registered users, as a parameter.
    def run(users: list[User]) -> None:
        while True:
            # Print welcome message and ask user to choose login or register
            CLI.print_big("Welcome to SuperMem!")
            CLI.print("Choose an option, or type \"exit\":\n")
            CLI.print("1. Login\n")
            CLI.print("2. Register\n")
            # User chooses an option
            option = CLI.ask_option([1, 2])
            # If option is None we need to exit
            if option is None:
                return
            # Redirect to login or register page based on the chosen option
            elif option == 1:
                user = LoginPage.run(users)
                # TODO: redirect to home page
            else:
                # Register a user and add it to the list of users
                user = RegisterPage.run()
                users.append(user)
                # After registration user is back to the index page so that they can login
                