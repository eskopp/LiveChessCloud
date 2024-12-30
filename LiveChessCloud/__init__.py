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
    """
    LiveChessCloud CLI

    A command-line interface for downloading and exporting chess games from LiveChessCloud.
    """
    pass


@main.command(name="help")
def help_command() -> None:
    """
    Display help information.
    """
    click.echo(f"{Fore.YELLOW}LiveChessCloud CLI Help{Fore.RESET}")
    click.echo(f"\n{Fore.YELLOW}Usage:{Fore.RESET}")
    click.echo(f"  LiveChessCloud <command> [arguments]")
    click.echo(f"\n{Fore.YELLOW}Commands:{Fore.RESET}")
    click.echo(
        f"  {Fore.CYAN}download{Fore.RESET} <url> - Download a chess game from the provided URL."
    )
    click.echo(
        f"  {Fore.CYAN}export{Fore.RESET} <url> [pgn] - Export a chess game to a PGN file from the provided URL."
    )
    click.echo(f"  {Fore.CYAN}help{Fore.RESET} - Display this help information.")
    click.echo(f"\n{Fore.YELLOW}Examples:{Fore.RESET}")
    click.echo(
        f"  LiveChessCloud download {Fore.CYAN}https://view.livechesscloud.com/#1eb49a34-ddb6-436a-b1bf-f4fc03c488d1{Fore.RESET}"
    )
    click.echo(
        f"  LiveChessCloud export {Fore.CYAN}https://view.livechesscloud.com/#1eb49a34-ddb6-436a-b1bf-f4fc03c488d1{Fore.RESET} {Fore.CYAN}output.pgn{Fore.RESET}"
    )
    click.echo(f"  LiveChessCloud help")


@main.command()
@click.argument("url")
def download(url: str) -> None:
    """
    Download a chess game from the provided URL.
    """
    if not re.match(r"https://view\.livechesscloud\.com/#\w+", url):
        click.echo(
            f"{Fore.RED}Error: Invalid URL format for download. Please provide a valid URL.{Fore.RESET}"
        )
        sys.exit(1)
    click.echo(f"{Fore.GREEN}Downloading game from URL: {url}{Fore.RESET}")
    result = asyncio.run(download.run_download(url))
    if result:
        click.echo(f"{Fore.GREEN}Download successful!{Fore.RESET}")
        click.echo(f"{Fore.CYAN}{result}{Fore.RESET}")
    else:
        click.echo(f"{Fore.RED}Download failed.{Fore.RESET}")


@main.command()
@click.argument("url")
@click.argument("pgn", default="LiveChessCloud.pgn")
def export(url: str, pgn: str) -> None:
    """
    Export a chess game to a PGN file from the provided URL.
    """
    if not re.match(r"https://view\.livechesscloud\.com/#\w+", url):
        click.echo(
            f"{Fore.RED}Error: Invalid URL format for export. Please provide a valid URL.{Fore.RESET}"
        )
        sys.exit(1)
    click.echo(f"{Fore.GREEN}Exporting game from URL: {url} to file: {pgn}{Fore.RESET}")
    try:
        export_command(url, pgn)
        click.echo(f"{Fore.GREEN}Export successful!{Fore.RESET}")
    except Exception as e:
        click.echo(f"{Fore.RED}Export failed: {str(e)}{Fore.RESET}")


if __name__ == "__main__":
    main(prog_name="livechesscloud")
