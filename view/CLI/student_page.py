from view.CLI.base_page import BasePage

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
        success, message = self.controller.register(name, email, password)
        print(message)
        self.pause()

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        success, _ = self.controller.login(email, password)
        if success:
            self.subject_menu()
        else:
            self.print_fail("Invalid credentials.")
            self.pause()

    def subject_menu(self):
        student = self.controller.current_student
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
                new_password = input("New Password: ")
                try:
                    student.change_password(new_password)
                    self.controller.save_current()
                    self.print_success("Password updated.")
                except ValueError as e:
                    self.print_fail(str(e))
                self.pause()
            elif choice == 'e':
                title = input("Subject Title: ")
                try:
                    subject = student.enrol_subject(title)
                    self.controller.save_current()
                    print(f"Enrolled in {subject.title} with mark {subject.mark} and grade {subject.grade}")
                except ValueError as e:
                    self.print_fail(str(e))
                self.pause()
            elif choice == 's':
                if not student.subjects:
                    print("No subjects enrolled.")
                else:
                    for s in student.subjects:
                        print(f"[{s.id}] {s.title} - Mark: {s.mark} - Grade: {s.grade}")
                    print(f"Average: {student.average_mark():.2f}")
                self.pause()
            elif choice == 'r':
                subject_id = input("Enter Subject ID to remove: ")
                if student.remove_subject(subject_id):
                    self.controller.save_current()
                    self.print_success(f"Subject {subject_id} removed.")
                else:
                    self.print_fail(f"Subject {subject_id} not found.")
                self.pause()
            elif choice == 'a':
                print(f"Average mark: {student.average_mark():.2f}")
                self.pause()
            elif choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")
                self.pause()
