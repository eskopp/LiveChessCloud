# export.py
from colorama import init, Fore, Style
from . import download
import asyncio

# Initialize colorama
init(autoreset=True)

def export(url: str, file: str) -> None:
    """
    Use the download function and write the output to the PGN file.
    """
    print(f"{Fore.YELLOW}{Style.BRIGHT}PGN file name:{Style.RESET_ALL} {file}")

    content = asyncio.run(download.run_download(url))
    # Content
    try:
        with open(file, "w+") as file:
            file.write(content)
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Error writing to the file {file}:{Style.RESET_ALL} {str(e)}")
