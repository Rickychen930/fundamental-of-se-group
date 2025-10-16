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
            choice = input("Choose: ").strip().lower()

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
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        success, message = self.controller.register(name, email, password)
        if success:
            self.print_success(message)
        else:
            self.print_fail(message)
        self.pause()

    def login(self):
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        # password = getpass.getpass("Password: ").strip() hidden the password
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
            choice = input("Choose: ").strip().lower()

            if choice == 'c':
                self.change_password(student)
            elif choice == 'e':
                self.enrol_subject(student)
            elif choice == 's':
                self.show_subjects(student)
            elif choice == 'r':
                self.remove_subject(student)
            elif choice == 'a':
                self.show_average(student)
            elif choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")
                self.pause()

    def change_password(self, student):
        new_password = input("New Password: ").strip()
        confirm_password = input("Re-enter New Password: ").strip()
        if new_password != confirm_password:
            self.print_fail("Passwords do not match.")
            self.pause()
            return

        try:
            student.change_password(new_password)
            self.controller.save_current()
            self.print_success("Password updated successfully.")
        except ValueError as e:
            self.print_fail(f"Error: {e}")
        self.pause()

    def enrol_subject(self, student):
        title = input("Subject Title: ").strip()
        try:
            subject = student.enrol_subject(title)
            self.controller.save_current()
            self.print_success(f"Enrolled in '{subject.title}' with mark {subject.mark} and grade {subject.grade}.")
        except ValueError as e:
            self.print_fail(f"Error: {e}")
        self.pause()

    def show_subjects(self, student):
        if not student.subjects:
            print("No subjects enrolled.")
        else:
            print("\n--- Enrolled Subjects ---")
            for s in student.subjects:
                print(f"[{s.id}] {s.title} - Mark: {s.mark} - Grade: {s.grade}")
            print(f"\nAverage: {student.average_mark():.2f}")
        self.pause()

    def remove_subject(self, student):
        subject_id = input("Enter Subject ID to remove: ").strip()
        if student.remove_subject(subject_id):
            self.controller.save_current()
            self.print_success(f"Subject '{subject_id}' removed.")
        else:
            self.print_fail(f"Subject '{subject_id}' not found.")
        self.pause()

    def show_average(self, student):
        print(f"Average mark: {student.average_mark():.2f}")
        self.pause()
