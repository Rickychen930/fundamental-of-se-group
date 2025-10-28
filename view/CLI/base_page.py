import os
import platform
from colorama import init, Fore

init(autoreset=True)

class BasePage:
    """Base class for CLI pages with common display helpers."""

    def clear_screen(self):
        """Clear the console window."""
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def print_fail(self, message):
        """Print an error message in red."""
        print(Fore.RED + message)

    def print_success(self, message):
        """Print a success or info message in yellow."""
        print(Fore.YELLOW + message)
