# export.py
from colorama import Fore, Back, Style
from . import download
import asyncio


def export(url: str, file: str) -> None:
    """
        Use the download function and write the output to the PGN file.
    """
    init(autoreset=True)
    print(f"{yellow_color}PGN file name:{Fore.RESET} {file}")
    content = asyncio.run(download.run_download(url))
    # Content
    try:
        with open(file, "w+") as file:
            file.write(content)
    except Exception as e:
        print(f"{Fore.RED}Error writing to the file {file}: {str(e)}")
