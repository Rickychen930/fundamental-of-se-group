from view.base_page import BasePage

class StudentPage(BasePage):
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        while True:
            self.clear_screen()
            print("--- Student Menu ---")
            print("(L) Login")
            print("(R) Register")
            print("(X) Exit")
            choice = input("Choose: ").lower()

            if choice == 'r':
                self.register()
            elif choice == 'l':
                self.login()
            elif choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")
                self.pause()

    def register(self):
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        result = self.controller.register(name, email, password)
        print(result)
        self.pause()

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        student = self.controller.login(email, password)
        if student:
            self.subject_menu(student)
        else:
            self.print_fail("Invalid credentials.")
            self.pause()

    def subject_menu(self, student):
        while True:
            self.clear_screen()
            print(f"--- Subject Menu for {student.name} ---")
            print("(C) Change Password")
            print("(E) Enrol Subject")
            print("(S) Show Enrolled Subjects")
            print("(R) Remove Subject")
            print("(A) Show Average Mark")
            print("(X) Exit")
            choice = input("Choose: ").lower()

            if choice == 'c':
                student.password = input("New Password: ")
                self.controller.update(student)
                self.print_success("Password updated.")
                self.pause()
            elif choice == 'e':
                print(student.enrol_subject())
                self.controller.update(student)
                self.pause()
            elif choice == 's':
                print(student.show_subjects())
                print(f"Average: {student.average_mark:.2f}")
                self.pause()
            elif choice == 'r':
                subject_id = input("Enter Subject ID to remove: ")
                print(student.remove_subject(subject_id))
                self.controller.update(student)
                self.pause()
            elif choice == 'a':
                print(f"Average mark: {student.average_mark:.2f}")
                self.pause()
            elif choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")
                self.pause()
