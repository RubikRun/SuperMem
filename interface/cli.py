import pwinput
from typing import List

# A class for common CLI functions, making sure CLI is used the same way across the whole application
class CLI:
    # Prefix that is printed before any message to indicate that it's printed by the application's CLI
    MSG_PREFIX = "---> "
    BIG_MSG_PREFIX = "-------> "
    BIG_MSG_SUFFIX = " <-------"

    # Prints a message on the console
    def print(msg: str) -> None:
        print(CLI.MSG_PREFIX, msg, end="", sep="")
    def print_big(msg: str) -> None:
        print(CLI.BIG_MSG_PREFIX, msg, CLI.BIG_MSG_SUFFIX, sep="")

    # Asks user for their input by printing some message and waiting for their answer.
    # Returns the answer.
    def ask_for(msg: str) -> str:
        CLI.print(msg)
        answer = input()
        return answer

    # Asks user for their password by printing some message and waiting for their answer.
    # Hides the input characters with '*'
    # Returns the password
    def ask_password(msg: str) -> str:
        password = pwinput.pwinput(prompt = CLI.MSG_PREFIX + msg, mask='*')
        return password

    # Asks for a CLI option. Repeats until user enters a valid option.
    # A valid option is an option from the given list of options.
    # Returns the entered valid option.
    def ask_option(options: List[int]) -> int:
        while True:
            try:
                option = int(CLI.ask_for("Option: "))
            except ValueError:
                option = -1
            if option in options:
                return option
            else:
                CLI.print("Invalid option. Try again.\n")