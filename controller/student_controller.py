from __future__ import annotations
from typing import Optional, Tuple, List
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
from models.user_model import User  # central validators


class StudentController:
    """
    Orchestrates student flows. No prints. No regex/business rules here.
    """
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

    # ---------- auth ----------
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

    # ---------- subject operations for current student ----------
    def enrol_subject(self, title: str) -> tuple[bool, str]:
        try:
            subject = self.current_student.enrol_subject(title)  # type: ignore
            self.save_current()
            return True, f"Enrolled in {subject.title} (ID {subject.id})"
        except Exception as e:
            return False, str(e)

    def remove_subject(self, subject_id: str) -> tuple[bool, str]:
        removed = self.current_student.remove_subject(subject_id)  # type: ignore
        if removed:
            self.save_current()
            return True, f"Removed subject {subject_id}"
        return False, "Subject not found."

    def change_password(self, new_password: str) -> tuple[bool, str]:
        try:
            self.current_student.change_password(new_password)  # type: ignore
            self.save_current()
            return True, "Password updated."
        except Exception as e:
            return False, str(e)

    def logout(self) -> None:
        self.current_student = None
