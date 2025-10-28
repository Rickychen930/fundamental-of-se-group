# controllers/subject_controller.py
from __future__ import annotations

import random
from typing import List, Optional, Tuple
from db.database import Database
from models.student_model import (Student, students_from_dicts, students_to_dicts, MAX_SUBJECTS)
from models.subject_model import Subject


class SubjectController:
    """  Subject flow  """

    def __init__(self, db: Database, current_student: Optional[Student] = None):
        self.db = db
        self.current_student: Optional[Student] = current_student

    def set_current_student(self, student: Student) -> None:
        self.current_student = student

    # ---------- core actions ----------

    def can_enrol_more(self) -> bool:
        """True if the student has fewer than MAX_SUBJECTS."""
        self._require_student()
        return len(self.current_student.subjects) < MAX_SUBJECTS  # type: ignore

    def enrol_auto(self) -> Tuple[bool, str, Optional[Subject]]:
        """
        Enrol in a random subject like 'Subject-541'.
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
        """Get the current student's subjects."""
        self._require_student()
        return list(self.current_student.subjects)  # type: ignore

    def remove_by_id(self, subject_id: str) -> Tuple[bool, str]:
        """Remove a subject using its ID. Returns (ok, message)."""
        self._require_student()
        student = self.current_student  # type: ignore
        removed = student.remove_subject(subject_id.strip())
        if removed:
            self._persist_current_student()
            return True, f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects"
        return False, "Subject not found."

    def average(self) -> Optional[float]:
        """Return the average mark, or None if there are no subjects."""
        self._require_student()
        return self.current_student.average_mark()  # type: ignore

    def change_password(self, new_pwd: str, confirm_pwd: str) -> Tuple[bool, str]:
        """Change password (checks both fields match). Returns (ok, message)."""
        self._require_student()
        if new_pwd.strip() != confirm_pwd.strip():
            return False, "Password does not match - try again"

        try:
            self.current_student.change_password(new_pwd.strip())  # type: ignore
            self._persist_current_student()
            return True, "Password updated"
        except ValueError as e:
            return False, str(e)

    # ---------- persistence ----------

    def _persist_current_student(self) -> None:
        """
        Save the current student's latest data back to the file.
        Keeps non-student records as they are.
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

    # ---------- utility ----------

    def _require_student(self) -> None:
        """Make sure a student is set before doing anything."""
        if not isinstance(self.current_student, Student):
            raise RuntimeError("No current student is set on SubjectController.")