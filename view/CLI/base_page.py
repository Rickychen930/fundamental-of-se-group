import os
import platform

# Simple ANSI color codes (work on most terminals)
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

class BasePage:
    """Base class for CLI pages with common display helpers."""

    def clear_screen(self):
        """Clear the console window."""
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def print_fail(self, message):
        """Print an error message in red."""
        print(f"{RED}{message}{RESET}")

    def print_success(self, message):
        """Print a success or info message in yellow."""
        print(f"{YELLOW}{message}{RESET}")
