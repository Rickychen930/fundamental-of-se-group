from __future__ import annotations

from typing import List, Dict, Optional
from view.CLI.base_page import BasePage
from models.student_model import Student
from models.subject_model import grade_from_mark, GRADE_ORDER


class AdminPage(BasePage):

    def __init__(self, controller):
        self.controller = controller

    # ---------- UI entry ----------
    def show(self):
        while True:
            print("\t\033[96mAdmin System (c/g/p/r/s/x): \033[0m", end="")
            choice = input().strip().lower()
            if choice == "c":
                self._clear_students_flow()
            elif choice == "g":
                self.show_grade_grouping()
            elif choice == "p":
                self.show_partition()
            elif choice == "r":
                self.remove_student_flow()
            elif choice == "s":
                self.show_all()
            elif choice == "x":
                break
            else:
                continue

    # ---------- Helper methods (formatting and grade conversion) ----------
    @staticmethod
    def _grade_from_avg(avg: Optional[float]) -> Optional[str]:
        if avg is None:
            return None
        return grade_from_mark(int(round(avg)))

    def _format_student_for_list(self, s: Student) -> str:
        """Exact one-line item used in Grade Grouping and PASS/FAIL Partition."""
        avg = s.average_mark()
        if avg is None:
            return f"{s.name} :: {s.id} --> GRADE: N/A - MARK: N/A"
        grade = self._grade_from_avg(avg) or "N/A"
        return f"{s.name} :: {s.id} --> GRADE: {grade} - MARK: {avg:.2f}"

    # ---------- Menu option flows ----------
    def _clear_students_flow(self):
        print("\t\033[93mClearing students database\033[0m")
        confirm = input("\t\033[91mAre you sure you want to clear the database (Y)ES/(N)O: \033[0m").strip().upper()
        if confirm == "Y":
            ok = self.controller.clear_all_students()
            if ok:
                print("\t\033[93mStudents data cleared\033[0m")

    def show_grade_grouping(self):
        grouped: Dict[str, List[Student]] = self.controller.group_by_grade()
        if not grouped or all(len(v) == 0 for v in grouped.values()):
            print("\t\t< Nothing to Display >")
            return

        print("\t\033[93mGrade Grouping\033[0m")
        # Enforce grade order
        for grade in GRADE_ORDER:
            students = grouped.get(grade, [])
            if not students:
                continue
            students = sorted(students, key=lambda s: (s.average_mark() or 0.0), reverse=True)
            body = ", ".join(self._format_student_for_list(s) for s in students)
            print(f"\t{grade} --> [{body}]")

    def show_partition(self):
        partitioned: Dict[str, List[Student]] = self.controller.partition_pass_fail()
        # Highest avg first
        for k in ("FAIL", "PASS"):
            if k in partitioned:
                partitioned[k].sort(key=lambda s: (s.average_mark() or 0.0), reverse=True)

        print("\t\033[93mPASS/FAIL Partition\033[0m")
        for status in ("FAIL", "PASS"):  
            students = partitioned.get(status, [])
            if not students:
                print(f"\t{status} --> []")
            else:
                body = ", ".join(self._format_student_for_list(s) for s in students)
                print(f"\t{status} --> [{body}]")

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
            print("\t\t< Nothing to Display >")
            return

        print("\t\033[93mStudent List\033[0m")
        for s in students:
            print(f"\t{s['name']}  ::  {s['id']}  -->  Email: {s['email']}")
