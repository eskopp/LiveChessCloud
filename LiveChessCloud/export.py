# export.py
from colorama import Fore, init
from . import download 
import asyncio

# Initialize Colorama to support colors on the console
init(autoreset=True)


def export(url: str, file: str) -> None:
    # Farbdefinitionen
    cyan_color = Fore.CYAN
    yellow_color = Fore.YELLOW

    # print(f"{cyan_color}Exporting is in progress for URL:{Fore.RESET} {url}")
    print(f"{yellow_color}PGN file name:{Fore.RESET} {file}")

    content = asyncio.run(download.run_download(url))
    
    try:
        with open(file, 'w+') as file:
            file.write(content)
        print(f'Content successfully written to the file {file}.')
    except Exception as e:
        print(f'Error writing to the file {file}: {str(e)}')
