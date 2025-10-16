from __future__ import annotations
from typing import List, Dict, Tuple
from db.database import Database
from models.admin_model import Admin
from models.student_model import Student, students_from_dicts, students_to_dicts

class AdminController:
    """
    Orchestrates Admin flows.
    """
    def __init__(self, db: Database):
        self.db = db
        self.admin = Admin.create("System Admin", "admin@university.com", "AdminPass123")

    # -------- Routing & Auth --------
    def login(self, email: str, password: str) -> tuple[bool, str | None]:
        ok = (email.strip().lower() == "admin@university.com") and self.admin.verify_password(password)
        return (ok, "admin") if ok else (False, None)

    # -------- Private I/O helpers (DRY) --------
    def _load_students(self) -> list[Student]:
        raw = self.db.read_from_file()
        return students_from_dicts(raw)

    def _write_students(self, students: list[Student]) -> None:
        raw_all = self.db.read_from_file()
        others = [d for d in raw_all if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))

    # -------- Admin operations (delegate rules to model) --------
    def list_students(self) -> list[dict]:
        students = self._load_students()
        return self.admin.list_students(students)

    def group_by_grade(self) -> dict[str, list[Student]]:
        students = self._load_students()
        return self.admin.group_by_grade(students)

    def partition_pass_fail(self) -> dict[str, list[Student]]:
        students = self._load_students()
        return self.admin.partition_pass_fail(students)

    def remove_student_by_id(self, student_id: str) -> bool:
        students = self._load_students()
        updated, removed = self.admin.remove_student_by_id(students, student_id)
        if removed:
            self._write_students(updated)
        return removed

    def clear_all_students(self) -> bool:
        self._write_students([])
        return True