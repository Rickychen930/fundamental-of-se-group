# -------------------------------------------------------------------
# Subject Controller 
# -------------------------------------------------------------------

from __future__ import annotations

import random
from typing import List, Optional, Tuple
from db.database import Database
from models.student_model import Student
from models.subject_model import Subject, MAX_SUBJECTS


class SubjectController:
    """Owns all subject-related actions for the currently logged-in student."""

    def __init__(self, db: Database, current_student: Optional[Student] = None):
        self.db = db
        self.current_student: Optional[Student] = current_student

    def set_current_student(self, student: Student) -> None:
        """Set or update the active student context."""
        self.current_student = student

    def can_enrol_more(self) -> bool:
        """True if the current student can enrol in more subjects."""
        if not self.current_student:
            return False
        return len(self.current_student.subjects) < MAX_SUBJECTS

    def enrol_auto(self) -> Tuple[bool, str, Optional[Subject]]:
        """
        Enrol in a random subject like 'Subject-541'.
        Returns (ok, message, subject|None).
        """
        if not self.current_student:
            return False, "Not logged in", None

        student = self.current_student

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
        except Exception as e:
            return False, str(e), None

    # ---------- main subject logic ----------

    def list_subjects(self) -> List[Subject]:
        """Get the current student's subjects (empty list if not logged in)."""
        if not self.current_student:
            return []
        return list(self.current_student.subjects)

    def remove_by_id(self, subject_id: str) -> Tuple[bool, str]:
        """Remove a subject using its ID. Returns (ok, message)."""
        if not self.current_student:
            return False, "Not logged in"

        student = self.current_student
        removed = student.remove_subject(subject_id.strip())
        if removed:
            self._persist_current_student()
            return True, f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects"
        return False, "Subject not found."

    def average(self) -> Optional[float]:
        """
        Return the current student's average mark, or None if not logged in
        or there are no subjects. (Thin wrapper around the model.)
        """
        if not self.current_student:
            return None
        return self.current_student.average_mark()

    # ---------- persistence ----------

    def _persist_current_student(self) -> None:
        """
        Persist the current student's latest state to the database.
        Replaces any existing record with the same id.
        """
        if not self.current_student:
            return

        raw = self.db.read_from_file()

        student_id = self.current_student.id
        out = [d for d in raw if str(d.get("id", "")).strip() != student_id]
        out.append(self.current_student.to_dict())

        self.db.write_to_file(out)
