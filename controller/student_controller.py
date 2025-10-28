from __future__ import annotations

import random
from typing import Optional, List
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
from models.user_model import User
from models.subject_model import MAX_SUBJECTS


class StudentController:
    """  Student flow  """

    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    # ---------- internals ----------

    def _load_students(self) -> List[Student]:
        """Read all students from the DB file."""
        raw = self.db.read_from_file()
        return students_from_dicts(raw)

    def _write_students(self, students: List[Student]) -> None:
        """Write students back to the DB file (keep non-student records)."""
        raw = self.db.read_from_file()
        others = [d for d in raw if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))

    # ---------- helpers used by the view ----------

    def find_by_email(self, email: str) -> Optional[Student]:
        """Find a student by email (case-insensitive)."""
        e = email.strip().lower()
        for s in self._load_students():
            if s.email.strip().lower() == e:
                return s
        return None

    def email_exists(self, email: str) -> bool:
        """Check if an email is already registered."""
        return self.find_by_email(email) is not None

    # ---------- login and register ----------

    def login(self, email: str, password: str) -> tuple[bool, Optional[str]]:
        """Validate formats, then log in and set current_student."""
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
        """Create a new student record if the email isn’t taken."""
        students = self._load_students()

        email_norm = email.strip().lower()
        if any(s.email.strip().lower() == email_norm for s in students):
            return False, f"Student {name.strip()} already exists"

        new_student = Student.create(name, email, password)
        students.append(new_student)
        self._write_students(students)
        return True, f"Enrolling Student {new_student.name}"

    # ---------- saving the current student ----------

    def save_current(self) -> None:
        """Write current_student back into the DB (if logged in)."""
        if not self.current_student:
            return
        students = self._load_students()
        for i, s in enumerate(students):
            if s.email.strip().lower() == self.current_student.email.strip().lower():
                students[i] = self.current_student
                break
        self._write_students(students)

    # ---------- direct subject ops (explicit title / id) ----------

    def enrol_subject(self, title: str) -> tuple[bool, str]:
        """Enrol using a provided title."""
        if not self.current_student:
            return False, "Not logged in"
        try:
            subject = self.current_student.enrol_subject(title)
            self.save_current()
            return True, f"Enrolled in {subject.title} (ID {subject.id})"
        except Exception as e:
            return False, str(e)

    def remove_subject(self, subject_id: str) -> tuple[bool, str]:
        """Remove a subject by id."""
        if not self.current_student:
            return False, "Not logged in"
        removed = self.current_student.remove_subject(subject_id.strip())
        if removed:
            self.save_current()
            return True, f"Removed subject {subject_id}"
        return False, "Subject not found."

    # ---------- methods the StudentPage calls ----------

    def list_subjects(self):
        """Return subjects for the logged-in student (or empty list)."""
        if not self.current_student:
            return []
        return self.current_student.subjects

    def enrol_auto(self):
        """
        Enrol in a random subject like 'Subject-123'.
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
            self.save_current()
            return True, f"You are now enrolled in {len(student.subjects)} out of {MAX_SUBJECTS} subjects", sub
        except Exception as e:
            return False, str(e), None

    def remove_by_id(self, subject_id: str):
        """Remove a subject by id. Returns (ok, message)."""
        if not self.current_student:
            return False, "Not logged in"
        ok = self.current_student.remove_subject(subject_id.strip())
        if ok:
            self.save_current()
            return True, f"You are now enrolled in {len(self.current_student.subjects)} out of {MAX_SUBJECTS} subjects"
        return False, "Subject not found."

    def change_password(self, new_password: str, confirm: str):
        """Change password with confirmation. Returns (ok, message)."""
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
        """Return average mark, or None if no subjects / not logged in."""
        if not self.current_student:
            return None
        return self.current_student.average_mark()
