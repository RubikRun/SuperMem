from interface.cli import CLI
from user import User

# A class for a home page of a user
# Each user has their own home page with their languages and words
class HomePage:
    # Creates a home page for the given user
    def __init__(self, user: User):
        self.user = user

    # Runs the home page
    def run(self, languages: list[str]) -> None:
        while True:
            # Print home page message and options for what to do
            CLI.print_big("Home Page of {}".format(self.user.username))
            # User chooses an option
            option = CLI.ask_option_num(
                "Choose an option, or type \"exit\":", [
                "Start learning a new language"
            ])
            # If option is None we need to exit
            if option is None:
                return
            elif option == 1:
                language = CLI.ask_option("What language do you want to start learning?", languages)