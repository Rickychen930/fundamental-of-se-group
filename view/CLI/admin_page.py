from __future__ import annotations
from view.CLI.base_page import BasePage
from colorama import Fore

class AdminPage(BasePage):
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        while True:
            print("\t\033[96mAdmin System (c/g/p/r/s/x): ", end="")
            choice = input().strip().lower()
            if choice == 'c':
                self._clear_students_flow()
            elif choice == 'g':
                self.show_group_by_grade()
            elif choice == 'p':
                self.show_partition()
            elif choice == 'r':
                self.remove_student_flow()
            elif choice == 's':
                self.show_all()
            elif choice == 'x':
                break
            else:
                self.print_fail("Invalid choice.")

    def _clear_students_flow(self):
        print("\t\033[93mClearing students database\033[0m")
        confirm = input("\t\033[91mAre you sure you want to clear the database (Y)ES/(N)O: \033[0m").strip().upper()
        if confirm == 'Y':
            ok = self.controller.clear_all_students()
            if ok:
                print("\t\033[93mStudents data cleared\033[0m")

    def show_group_by_grade(self):
        grouped = self.controller.group_by_grade()
        if not grouped or all(len(v) == 0 for v in grouped.values()):
            print("\t\t< Nothing to Display >")
            return
        print("\t\033[93mGrade Grouping\033[0m")
        for grade, students in grouped.items():
            if not students:
                continue
            details = []
            for s in students:
                avg = s.average_mark()
                details.append(f"{s.name} :: {s.id} --> GRADE: {grade} - MARK: {avg:.2f}" if avg is not None else f"{s.name} :: {s.id} --> GRADE: {grade}")
            print(f"\t{grade}  -->  [{', '.join(details)}]")

    def show_partition(self):
        partitioned = self.controller.partition_pass_fail()
        if not partitioned or all(len(v) == 0 for v in partitioned.values()):
            print("\t\t< Nothing to Display >")
            return
        print("\t\033[93mPartitioned by Pass/Fail\033[0m")
        for status, students in partitioned.items():
            for s in students:
                color = Fore.GREEN if status == "PASS" else Fore.RED
                print(color + f"\t{s.name} - {status}")

    def remove_student_flow(self):
        sid = input("\tRemove by ID: ").strip()
        removed = self.controller.remove_student_by_id(sid)
        if removed:
            self.print_success(f"\tRemoving Student {sid} Account")
        else:
            self.print_fail(f"\tStudent {sid} does not exist")

    def show_all(self):
        students = self.controller.list_students()
        if not students:
            print("\t\t < Nothing to Display >")
            return
        print("\t\033[93mStudent List\033[0m")
        for s in students:
            print(f"\t{s['name']}  ::  {s['id']}  -->  Email: {s['email']}")