# controllers/subject_controller.py
from __future__ import annotations

import random
from typing import List, Optional, Tuple

from db.database import Database
from models.student_model import (
    Student,
    students_from_dicts,
    students_to_dicts,
    MAX_SUBJECTS,
)
from models.subject_model import Subject


class SubjectController:
    """
    Handles subject operations for the *current* logged-in student and persists
    changes back to db/students.data.
    """

    def __init__(self, db: Database, current_student: Optional[Student] = None):
        self.db = db
        self.current_student: Optional[Student] = current_student

    # ---------- Session binding ----------
    def set_current_student(self, student: Student) -> None:
        self.current_student = student

    # ---------- Core actions ----------
    def can_enrol_more(self) -> bool:
        self._require_student()
        return len(self.current_student.subjects) < MAX_SUBJECTS  # type: ignore

    def enrol_auto(self) -> Tuple[bool, str, Optional[Subject]]:
        """
        Enrols the current student in a randomly named subject like 'Subject-541'.
        Returns (ok, message, subject|None).
        """
        self._require_student()
        student = self.current_student  # type: ignore

        if len(student.subjects) >= MAX_SUBJECTS:
            return False, "students are allowed to enrol in 4 subjects only", None

        title = f"Subject-{random.randint(1, 999)}"
        try:
            sub = student.enrol_subject(title)
            self._persist_current_student()
            enrolled = len(student.subjects)
            return True, f"You are now enrolled in {enrolled} out of {MAX_SUBJECTS} subjects", sub
        except ValueError as e:
            return False, str(e), None

    def list_subjects(self) -> List[Subject]:
        """Return the student's subjects in the current session."""
        self._require_student()
        return list(self.current_student.subjects)  # type: ignore

    def remove_by_id(self, subject_id: str) -> Tuple[bool, str]:
        """
        Removes a subject by its ID. Returns (ok, message).
        """
        self._require_student()
        student = self.current_student  # type: ignore
        removed = student.remove_subject(subject_id.strip())
        if removed:
            self._persist_current_student()
            return True, f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects"
        return False, "Subject not found."

    def average(self) -> Optional[float]:
        """Compute the student's average or None if no subjects."""
        self._require_student()
        return self.current_student.average_mark()  # type: ignore

    def change_password(self, new_pwd: str, confirm_pwd: str) -> Tuple[bool, str]:
        """
        Change password with confirmation. Re-uses Student/User validation rules.
        Returns (ok, message). Reusing same password is allowed per brief.
        """
        self._require_student()
        if new_pwd.strip() != confirm_pwd.strip():
            return False, "Password does not match - try again"

        try:
            self.current_student.change_password(new_pwd.strip())  # type: ignore
            self._persist_current_student()
            return True, "Password updated"
        except ValueError as e:
            return False, str(e)

    def _persist_current_student(self) -> None:
        """
        Persist the current student's latest data to the database file.

        Reads all existing records, replaces the matching student entry
        (by ID), and writes the updated list back to `students.data`.
        Non-student records remain unchanged. If the student is missing,
        their record is appended.

        Args:
            None

        Returns:
            None

        Raises:
            RuntimeError: If no current student is set.
            IOError: If reading or writing to the file fails.
        """
        self._require_student()
        student = self.current_student

        raw = self.db.read_from_file()
        out = []
        found = False

        for d in raw:
            if d.get("role") != "student":
                out.append(d)
                continue

            sid = str(d.get("id", "")).strip()
            if sid == student.id:
                out.append(student.to_dict())
                found = True
            else:
                out.append(d)

        if not found:
            out.append(student.to_dict())

        self.db.write_to_file(out)

    # ---------- Utilities ----------
    def _require_student(self) -> None:
        if not isinstance(self.current_student, Student):
            raise RuntimeError("No current student is set on SubjectController.")
