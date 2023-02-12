import pwinput

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
        print("\n", CLI.BIG_MSG_PREFIX, msg, CLI.BIG_MSG_SUFFIX, sep="")

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

    # Asks for a CLI option. Returns the number of the chosen option.
    def ask_option_num(msg: str, options: list[str]) -> int:
        CLI.print(msg + "\n")
        nums = []
        # Traverse options and print each one with a number in front
        for idx, option in enumerate(options):
            num = idx + 1
            CLI.print(str(num) + ". " + option + "\n")
            nums.append(num)
        # Ask user to choose from the listed options
        while True:
            answer = CLI.ask_for("Option: ")
            if answer == "exit":
                return None
            try:
                num = int(answer)
            except ValueError:
                num = -1
            if num in nums:
                return num
            else:
                CLI.print("Invalid option. Try again.\n")

    # Asks for a CLI option. Returns the chosen option.
    def ask_option(msg: str, options: list[str]) -> str:
        num = CLI.ask_option_num(msg, options)
        if num is None:
            return None
        return options[num - 1]