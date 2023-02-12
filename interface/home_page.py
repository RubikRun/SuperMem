from interface.cli import CLI
from user import User

# A class for a home page of a user
# Each user has their own home page with their languages and words
class HomePage:
    # Creates a home page for the given user
    def __init__(self, user: User):
        self.user = user

    # Runs the home page
    def run(self) -> None:
        while True:
            # Print home page message
            CLI.print_big("Home Page of {}".format(self.user.username))
            CLI.print("Choose an option, or type \"exit\":\n")
            # User chooses an option
            option = CLI.ask_option([])
            # If option is None we need to exit
            if option is None:
                return