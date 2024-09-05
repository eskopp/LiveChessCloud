# LiveChessCloud/__init__.py

import sys
import re
from colorama import init, Fore
from . import help
from . import download
from . import export
import asyncio


# Initialize Colorama to support colors on the console
init(autoreset=True)


def main() -> None:
    # Check if 'help' or '--version' is the only argument
    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            # Call the help function if only 'help' is provided as an argument
            help.help()
        elif sys.argv[1] in ("-v", "--version"):
            print(f"LiveChessCloud {__version__}")
        else:
            print(f"{Fore.RED}Unknown option: {sys.argv[1]}")
            sys.exit(1)
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
        if action == "download":
            if not re.match(r"https://view\.livechesscloud\.com/#\w+", url):
                print(
                    f"{Fore.RED}Error: Invalid URL format for export. Please provide a valid URL."
                )
                sys.exit(1)
            print(asyncio.run(download.run_download(url)))

        elif action == "export":
            # Check for the presence of a valid URL in the second argument
            if not re.match(r"https://view\.livechesscloud\.com/#\w+", url):
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
