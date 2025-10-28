from __future__ import annotations

import random
from typing import Optional, List
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
from models.user_model import User
from models.subject_model import MAX_SUBJECTS


class StudentController:
    """Orchestrates student flows. No prints; exposes methods for the view."""

    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    # ---------- internal helpers ----------

    def _load_students(self) -> List[Student]:
        raw = self.db.read_from_file()
        return students_from_dicts(raw)

    def _write_students(self, students: List[Student]) -> None:
        raw = self.db.read_from_file()
        others = [d for d in raw if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))

    # ---------- utilities for the View ----------

    def find_by_email(self, email: str) -> Optional[Student]:
        """Return the Student with this email, or None."""
        e = email.strip().lower()
        for s in self._load_students():
            if s.email.strip().lower() == e:
                return s
        return None

    def email_exists(self, email: str) -> bool:
        return self.find_by_email(email) is not None

    # ---------- login and register ----------

    def login(self, email: str, password: str) -> tuple[bool, Optional[str]]:
        # Validate formats via User validators (keeps rules out of controller)
        if not (User.validate_email(email) and User.validate_password(password)):
            return False, "bad_format"

        email_norm = email.strip().lower()
        for s in self._load_students():
            if s.email.strip().lower() == email_norm:
                if s.verify_password(password):
                    self.current_student = s
                    return True, "student"
                return False, "bad_password"
        return False, "no_such_user"

    def register(self, name: str, email: str, password: str) -> tuple[bool, str]:
        students = self._load_students()

        email_norm = email.strip().lower()
        if any(s.email.strip().lower() == email_norm for s in students):
            # Message shape matches earlier transcripts; the view should normally
            # call email_exists() before asking for the name.
            return False, f"Student {name.strip()} already exists"

        # Delegate validation & creation to the model
        new_student = Student.create(name, email, password)
        students.append(new_student)
        self._write_students(students)
        return True, f"Enrolling Student {new_student.name}"

    # ---------- persistence of current student ----------

    def save_current(self) -> None:
        if not self.current_student:
            return
        students = self._load_students()
        for i, s in enumerate(students):
            if s.email.strip().lower() == self.current_student.email.strip().lower():
                students[i] = self.current_student
                break
        self._write_students(students)

    # ---------- subject operations for current student (direct) ----------

    def enrol_subject(self, title: str) -> tuple[bool, str]:
        """Enrol with an explicit title."""
        if not self.current_student:
            return False, "Not logged in"
        try:
            subject = self.current_student.enrol_subject(title)
            self.save_current()
            return True, f"Enrolled in {subject.title} (ID {subject.id})"
        except Exception as e:
            return False, str(e)

    def remove_subject(self, subject_id: str) -> tuple[bool, str]:
        """Remove by subject id (direct)."""
        if not self.current_student:
            return False, "Not logged in"
        removed = self.current_student.remove_subject(subject_id.strip())
        if removed:
            self.save_current()
            return True, f"Removed subject {subject_id}"
        return False, "Subject not found."

    # ---------- thin helpers used by StudentPage ----------

    def list_subjects(self):
        """Return the current student's subjects (or empty list)."""
        if not self.current_student:
            return []
        return self.current_student.subjects

    def enrol_auto(self):
        """
        Auto-enrol in a randomly named subject (Subject-###).
        Returns: (ok, msg, subject|None)
        """
        if not self.current_student:
            return False, "Not logged in", None

        student = self.current_student
        if len(student.subjects) >= MAX_SUBJECTS:
            return False, "students are allowed to enrol in 4 subjects only", None

        title = f"Subject-{random.randint(1, 999)}"
        try:
            sub = student.enrol_subject(title)
            self.save_current()
            return True, f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects", sub
        except Exception as e:
            return False, str(e), None

    def remove_by_id(self, subject_id: str):
        """Remove a subject by id. Returns (ok, msg)."""
        if not self.current_student:
            return False, "Not logged in"
        ok = self.current_student.remove_subject(subject_id.strip())
        if ok:
            self.save_current()
            return True, f"You are now enrolled in {len(self.current_student.subjects)} out of {MAX_SUBJECTS} subjects"
        return False, "Subject not found."

    def change_password(self, new_password: str, confirm: str):
        """Change password with confirmation. Returns (ok, msg)."""
        if not self.current_student:
            return False, "Not logged in"
        if new_password.strip() != confirm.strip():
            return False, "Password does not match - try again"
        try:
            self.current_student.change_password(new_password.strip())
            self.save_current()
            return True, "Password updated"
        except Exception as e:
            return False, str(e)

    def average(self):
        """Average mark for the current student, or None."""
        if not self.current_student:
            return None
        return self.current_student.average_mark()
