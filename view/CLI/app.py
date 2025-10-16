from view.CLI.admin_page import AdminPage
from view.CLI.student_page import StudentPage
from controller.admin_controller import AdminController
from controller.student_controller import StudentController
from db.database import Database

class App:
    def __init__(self):
        self.db = Database()
        self.admin_controller = AdminController(self.db)
        self.student_controller = StudentController(self.db)

        self.admin_page = AdminPage(self.admin_controller)
        self.student_page = StudentPage(self.student_controller)

    def run(self):
        self._clear_screen()
        while True:
            # University System prompt
            print("\033[96mUniversity System: (A)dmin, (S)tudent, or X : ", end="")
            choice = input().strip().upper()

            # Admin system entry point
            if choice == 'A':
                self.admin_page.show()

            # Student system entry point
            elif choice == 'S':
                self.student_page.show()

            # Exit menu
            elif choice == 'X':
                print("\033[93mThank You\033[0m")
                break
            
            # Loop back to menu if incorrect selection
            else:
                continue
        

    def _clear_screen(self):
        # Works on most terminals
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_fail(self, message):
        print(f"[ERROR] {message}")

    def _pause(self):
        input("Press Enter to continue...")
