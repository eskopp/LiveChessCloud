# help.py
from colorama import Fore


def help() -> None:
    url_example = (
        "https://view.livechesscloud.com/#1eb49a34-ddb6-436a-b1bf-f4fc03c488d1"
    )

    print(f"{Fore.YELLOW}Usage:{Fore.RESET}")
    print(f"  LiveChessCloud <Action> <URL>")
    print(f"\n{Fore.YELLOW}Possible actions:{Fore.RESET}")
    print(
        f"  {Fore.CYAN}download{Fore.RESET} - Download is in progress for the provided URL."
    )
    print(
        f"  {Fore.CYAN}export{Fore.RESET}   - Exporting is in progress for the provided URL and expects a PGN file."
    )
    print(f"  {Fore.CYAN}help{Fore.RESET}     - Display this help information.")

    # Example with 'download'
    print(f"\n{Fore.YELLOW}Example with 'download'{Fore.RESET}:")
    print(f'  LiveChessCloud download {Fore.CYAN}"{url_example}"{Fore.RESET}')

    # Example with 'export'
    print(f"\n{Fore.YELLOW}Example with 'export'{Fore.RESET}:")
    print(
        f'  LiveChessCloud export {Fore.CYAN}"{url_example}" {Fore.CYAN}"output.pgn"{Fore.RESET}'
    )

    # Example with 'help'
    print(f"\n{Fore.YELLOW}Example with 'help'{Fore.RESET}:")
    print("  LiveChessCloud help")

    print(f"\n{Fore.YELLOW}Note:{Fore.RESET}")
    print(
        f"  {Fore.YELLOW}For the 'export' action, the provided URL should be followed by the PGN file name.{Fore.RESET}"
    )
