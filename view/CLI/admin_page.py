from view.CLI.base_page import BasePage
from colorama import Fore

class AdminPage(BasePage):
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        while True:
            self.clear_screen()
            print("--- Admin Menu ---")
            print("(C) Clear Database")
            print("(G) Group Students by Grade")
            print("(P) Partition Students (PASS/FAIL)")
            print("(R) Remove Student by ID")
            print("(S) Show All Students")
            print("(X) Exit")
            choice = input("Choose: ").lower()

            if choice == 'c':
                self.controller.clear_all_students()
                self.print_success("Database cleared.")
                self.pause()
            elif choice == 'g':
                self.group_by_grade()
            elif choice == 'p':
                self.partition()
            elif choice == 'r':
                self.remove_student()
            elif choice == 's':
                self.show_all()
            elif choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")
                self.pause()

    def group_by_grade(self):
        grouped = self.controller.group_by_grade()
        if not grouped:
            print("No grade data available.")
        else:
            for grade, students in grouped.items():
                names = [s.name for s in students]
                print(f"{grade}: {', '.join(names)}")
        self.pause()

    def partition(self):
        partitioned = self.controller.partition_pass_fail()
        if not partitioned:
            print("No student data available.")
        else:
            for status, students in partitioned.items():
                for s in students:
                    color = Fore.GREEN if status == "PASS" else Fore.RED
                    print(color + f"{s.name} - {status}")
        self.pause()

    def remove_student(self):
        sid = input("Enter Student ID to remove: ")
        removed = self.controller.remove_student_by_id(sid)
        if removed:
            self.print_success(f"Student {sid} removed.")
        else:
            self.print_fail(f"Student {sid} not found.")
        self.pause()

    def show_all(self):
        students = self.controller.list_students()
        if not students:
            print("No students found.")
        else:
            for s in students:
                print(f"{s['id']} - {s['name']} - {s['email']}")
        self.pause()
