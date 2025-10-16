from view.CLI.base_page import BasePage

class StudentPage(BasePage):
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        while True:
            print("\t\033[96mStudent System (l/r/x) : ", end="")
            student_choice = input().strip().lower()

            if student_choice == 'r':
                self.register()
            elif student_choice == 'l':
                self.login()
            elif student_choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")

    def register(self):
        print("\t\033[92mStudent Sign Up\033[0m")

        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()

            valid, msg = self.controller.validate_credentials(email, password)
            if not valid:
                print(f"\t\033[91m{msg}\033[0m")
                continue

            print(f"\t\033[93m{msg}\033[0m")
            break

        name = input("\tName: ").strip()
        print(f"\t\033[93mEnrolling Student {name}\033[0m")
        success, message = self.controller.register(name, email, password)

        if success and message:
            print(f"\t\033[92m{message}\033[0m")


    def login(self):
        print("\t\033[92mStudent Sign In\033[0m")
        email = input("\tEmail: ").strip()
        password = input("\tPassword: ").strip()
        success, _ = self.controller.login(email, password)
        if success:
            self.subject_menu()
        else:
            self.print_fail("Invalid credentials.")

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

    def change_password(self, student):
        new_password = input("New Password: ").strip()
        confirm_password = input("Re-enter New Password: ").strip()
        if new_password != confirm_password:
            self.print_fail("Passwords do not match.")
            return

        try:
            student.change_password(new_password)
            self.controller.save_current()
            self.print_success("Password updated successfully.")
        except ValueError as e:
            self.print_fail(f"Error: {e}")

    def enrol_subject(self, student):
        title = input("Subject Title: ").strip()
        try:
            subject = student.enrol_subject(title)
            self.controller.save_current()
            self.print_success(f"Enrolled in '{subject.title}' with mark {subject.mark} and grade {subject.grade}.")
        except ValueError as e:
            self.print_fail(f"Error: {e}")

    def show_subjects(self, student):
        if not student.subjects:
            print("No subjects enrolled.")
        else:
            print("\n--- Enrolled Subjects ---")
            for s in student.subjects:
                print(f"[{s.id}] {s.title} - Mark: {s.mark} - Grade: {s.grade}")
            print(f"\nAverage: {student.average_mark():.2f}")

    def remove_subject(self, student):
        subject_id = input("Enter Subject ID to remove: ").strip()
        if student.remove_subject(subject_id):
            self.controller.save_current()
            self.print_success(f"Subject '{subject_id}' removed.")
        else:
            self.print_fail(f"Subject '{subject_id}' not found.")

    def show_average(self, student):
        print(f"Average mark: {student.average_mark():.2f}")