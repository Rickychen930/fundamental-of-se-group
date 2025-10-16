import os
import platform
from colorama import init, Fore

init(autoreset=True)

class BasePage:
    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def print_fail(self, message):
        print(Fore.RED + message)

    def print_success(self, message):
        print(Fore.GREEN + message)
