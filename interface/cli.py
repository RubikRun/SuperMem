# A class for common CLI functions, making sure CLI is used the same way across the whole application
class CLI:
    # Prints a message on the console with an appropriate prefix indicating that it's printed by the application
    def print(msg: str) -> None:
        print("---> ", msg, end="", sep="")
    # Asks user for their input by printing some message and waiting for their answer.
    # Returns the answer.
    def ask_for(msg: str) -> str:
        CLI.print(msg)
        answer = input()
        return answer
