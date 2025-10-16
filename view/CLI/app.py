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
        while True:
            self._clear_screen()
            print("=== University Menu ===")
            print("(A) Admin")
            print("(S) Student")
            print("(X) Exit")
            choice = input("Choose: ").strip().upper()

            if choice == 'A':
                self.admin_page.show()
            elif choice == 'S':
                self.student_page.show()
            elif choice == 'X':
                print("Goodbye!")
                break
            else:
                self._print_fail("Invalid choice.")
                self._pause()

    def _clear_screen(self):
        # Works on most terminals
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_fail(self, message):
        print(f"[ERROR] {message}")

    def _pause(self):
        input("Press Enter to continue...")
