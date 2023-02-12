import pwinput

# A class for common CLI functions, making sure CLI is used the same way across the whole application
class CLI:
    # Prefix that is printed before any message to indicate that it's printed by the application's CLI
    MSG_PREFIX = "---> "

    # Prints a message on the console
    def print(msg: str) -> None:
        print(CLI.MSG_PREFIX, msg, end="", sep="")

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