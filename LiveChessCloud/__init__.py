# LiveChessCloud/__init__.py

import sys
import re
from colorama import init, Fore
from . import help
from . import download
from . import export

# Initialize Colorama to support colors on the console
init(autoreset=True)


def main() -> None:
    # Check if 'help' is the only argument
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        # Call the help function if only 'help' is provided as an argument
        help.help()
    else:
        # Check if an adequate number of arguments are provided for other actions
        if len(sys.argv) < 3:
            print(f"{Fore.RED}Usage: python -m LiveChessCloud <Action> <URL>")
            print(f"Possible actions: {Fore.CYAN}download, export, help")
            sys.exit(1)

        # Extract the provided action and URL
        action = sys.argv[1]
        url = sys.argv[2]
        pgn = "LiveChessCloud.pgn"
        if len(sys.argv) == 4 and sys.argv[3]:
            pgn = sys.argv[3]

        # Check which action was specified
        if action == "download":  #
            if not re.match(r"https://view.livechesscloud.com/#\w+", url):
                print(
                    f"{Fore.RED}Error: Invalid URL format for export. Please provide a valid URL."
                )
                sys.exit(1)
            # Insert logic for download here
            # No other output
            # print(f"{Fore.GREEN}Downloading is in progress for URL: {url}")
            download.download(url)
        elif action == "export":
            # Check for the presence of a valid URL in the second argument
            if not re.match(r"https://view.livechesscloud.com/#\w+", url):
                print(
                    f"{Fore.RED}Error: Invalid URL format for export. Please provide a valid URL."
                )
                sys.exit(1)
            # Insert logic for export here
            print(f"{Fore.GREEN}Exporting is in progress for URL: {url}")
            export.export(url, pgn)
        else:
            print(
                f"{Fore.RED}Error: Invalid action. Use '{Fore.CYAN}help{Fore.RED}' for assistance."
            )


if __name__ == "__main__":
    main()
