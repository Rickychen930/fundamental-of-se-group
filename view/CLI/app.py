from view.CLI.admin_page import AdminPage
from view.CLI.student_page import StudentPage
from controller.admin_controller import AdminController
from controller.student_controller import StudentController
from controller.subject_controller import SubjectController 
from db.database import Database


class App:
    """Main coordinator for the CLI University System."""

    def __init__(self):
        """Set up database, controllers, and views."""
        self.db = Database()
        # Controllers
        self.admin_controller = AdminController(self.db)
        self.student_controller = StudentController(self.db)
        self.subject_controller = SubjectController(self.db) 

        # Pages
        self.admin_page = AdminPage(self.admin_controller)
        self.student_page = StudentPage(self.student_controller, self.subject_controller)

    def run(self):
        """Display main menu and route to Admin or Student systems."""
        self._clear_screen()
        while True:
            print("\033[96mUniversity System: (A)dmin, (S)tudent, or X : \033[0m", end="")
            choice = input().strip().upper()

            if choice == 'A':        # Admin system
                self.admin_page.show()
            elif choice == 'S':      # Student system
                self.student_page.show()
            elif choice == 'X':      # Exit
                print("\033[93mThank You\033[0m")
                break
            else:                    # Invalid input
                continue

    # ---------- Utilities ----------
    def _clear_screen(self):
        """Clear the terminal screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_fail(self, message):
        """Show an error message."""
        print(f"[ERROR] {message}")

    def _pause(self):
        """Wait for user input before continuing."""
        input("Press Enter to continue...")
