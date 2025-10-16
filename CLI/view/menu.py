from view.admin_page import AdminPage
from view.student_page import StudentPage
from view.base_page import BasePage
from controller.admin_controller import AdminController
from controller.student_controller import StudentController

class UniversityApp(BasePage):
    def __init__(self):
        self.admin_page = AdminPage(AdminController)
        self.student_page = StudentPage(StudentController)

    def run(self):
        while True:
            self.clear_screen()
            print("=== University Menu ===")
            print("(A) Admin")
            print("(S) Student")
            print("(X) Exit")
            choice = input("Choose: ").upper()

            if choice == 'A':
                self.admin_page.show()
            elif choice == 'S':
                self.student_page.show()
            elif choice == 'X':
                print("Goodbye!")
                break
            else:
                self.print_fail("Invalid choice.")
                self.pause()
