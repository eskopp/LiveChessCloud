# export.py
from colorama import Fore, init

# Initialize Colorama to support colors on the console
init(autoreset=True)

def export(url: str, file: str) -> None:
    # Farbdefinitionen
    cyan_color = Fore.CYAN
    yellow_color = Fore.YELLOW

    print(f"{cyan_color}Exporting is in progress for URL:{Fore.RESET} {url}")
    print(f"{yellow_color}PGN file name:{Fore.RESET} {file}")

  # TODO: Code