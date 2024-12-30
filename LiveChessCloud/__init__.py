# LiveChessCloud/__init__.py

import sys
import re
import click
from colorama import init, Fore
from . import help
from . import download
from .export import export as export_command
import asyncio

# Initialize Colorama to support colors on the console
init(autoreset=True)

@click.group()
def main() -> None:
    pass

@main.command()
def help() -> None:
    help.help()

@main.command()
@click.argument('url')
def download(url: str) -> None:
    if not re.match(r"https://view\.livechesscloud\.com/#\w+", url):
        print(
            f"{Fore.RED}Error: Invalid URL format for download. Please provide a valid URL."
        )
        sys.exit(1)
    print(asyncio.run(download.run_download(url)))

@main.command()
@click.argument('url')
@click.argument('pgn', default="LiveChessCloud.pgn")
def export(url: str, pgn: str) -> None:
    if not re.match(r"https://view\.livechesscloud\.com/#\w+", url):
        print(
            f"{Fore.RED}Error: Invalid URL format for export. Please provide a valid URL."
        )
        sys.exit(1)
    print(f"{Fore.GREEN}Exporting is in progress for URL: {url}")
    export_command(url, pgn)

if __name__ == "__main__":
    main()
