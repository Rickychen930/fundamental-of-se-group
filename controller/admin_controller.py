from __future__ import annotations

from typing import List, Dict, Tuple
from db.database import Database
from models.admin_model import Admin
from models.student_model import Student, students_from_dicts, students_to_dicts


class AdminController:
    """Handles admin features like viewing, grouping, and removing students."""

    def __init__(self, db: Database):
        """Set up the admin account and connect to the database."""
        self.db = db
        self.admin = Admin.create("System Admin", "admin@university.com", "AdminPass123")

    # ---------- login ----------

    def login(self, email: str, password: str) -> tuple[bool, str | None]:
        """Check admin email and password."""
        ok = (email.strip().lower() == "admin@university.com") and self.admin.verify_password(password)
        return (ok, "admin") if ok else (False, None)

    # ---------- private file helpers ----------

    def _load_students(self) -> list[Student]:
        """Read all student data from the file."""
        raw = self.db.read_from_file()
        return students_from_dicts(raw)

    def _write_students(self, students: list[Student]) -> None:
        """Write updated student data back to the file (keep non-student records)."""
        raw_all = self.db.read_from_file()
        others = [d for d in raw_all if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))

    # ---------- main admin actions ----------

    def list_students(self) -> list[dict]:
        """Return a list of all students with their details."""
        students = self._load_students()
        return self.admin.list_students(students)

    def group_by_grade(self) -> dict[str, list[Student]]:
        """Group students by their grade (HD, D, C, P, F)."""
        students = self._load_students()
        return self.admin.group_by_grade(students)

    def partition_pass_fail(self) -> dict[str, list[Student]]:
        """Split students into pass and fail groups."""
        students = self._load_students()
        return self.admin.partition_pass_fail(students)

    def remove_student_by_id(self, student_id: str) -> bool:
        """Remove a student by their ID and save the changes."""
        students = self._load_students()
        updated, removed = self.admin.remove_student_by_id(students, student_id)
        if removed:
            self._write_students(updated)
        return removed

    def clear_all_students(self) -> bool:
        """Delete all student records from the database."""
        self._write_students([])
        return True
