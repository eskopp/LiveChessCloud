from colorama import init, Fore, Style

# Initialize colorama
init()

def print_header(text):
    print(Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL)

def print_info(text):
    print(Fore.CYAN + text + Style.RESET_ALL)

def print_error(text):
    print(Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)

# Example usage
if __name__ == "__main__":
    print_header("This is a header")
    print_info("This is an info message")
    print_error("This is an error message")
