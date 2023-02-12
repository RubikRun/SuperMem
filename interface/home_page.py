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
                "Start learning a new language",
                "What languages am I learning?"
            ])
            # If option is None we need to exit
            if option is None:
                return
            elif option == 1:
                self.start_learning_new_language(languages)
            elif option == 2:
                self.show_active_languages()

    # Asks a user what language they want to start learning, gives them a list of only the languages that are available for them.
    # Adds the chosen language to the user's active languages
    def start_learning_new_language(self, languages: list[str]) -> None:
        # User cannot be learning their own language or a language they're already learning,
        # so remove those from the list of languages
        learnable_languages = languages.copy()
        learnable_languages.remove(self.user.main_language)
        for language in self.user.active_languages:
            learnable_languages.remove(language)
        language = CLI.ask_option("What language do you want to start learning?", learnable_languages)
        if language is None:
            return
        self.user.active_languages.append(language)
        CLI.print("Okay. {} added to your active languages.\n".format(language))

    # Shows the user their active languages.
    def show_active_languages(self) -> None:
        if not self.user.active_languages:
            CLI.print("You are not learning any languages.\n")
            return
        languages_str = self.user.active_languages[0]
        for language in self.user.active_languages[1:]:
            languages_str += ", " + language
        CLI.print("You are learning {}\n".format(languages_str))