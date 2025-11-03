from __future__ import annotations
from typing import Optional, List
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
from models.user_model import User


class StudentController:
    """Owns student identity/session and profile updates (no subject ops here)."""

    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    # ---------- Internal Helpers ----------

    def _load_students(self) -> List[Student]:
        """Read all students from the DB file."""
        raw = self.db.read_from_file()
        return students_from_dicts(raw)

    def _write_students(self, students: List[Student]) -> None:
        """Overwrite the DB with exactly these students."""
        self.db.write_to_file(students_to_dicts(students))

    def _save_current_profile(self) -> None:
        """
        Persist non-subject changes to the current student (e.g., password).
        Subject mutations should be persisted by SubjectController.
        """
        if not self.current_student:
            return

        students = self._load_students()
        students = [s for s in students if s.id != self.current_student.id]
        students.append(self.current_student)

        self._write_students(students)

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
    
    # ---------- Below is the Student Logic ----------

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

    def change_password(self, new_password: str, confirm: str) -> tuple[bool, str]:
        """Change password with confirmation. Returns (ok, message)."""
        if not self.current_student:
            return False, "Not logged in"
        if new_password.strip() != confirm.strip():
            return False, "Password does not match - try again"
        try:
            self.current_student.change_password(new_password.strip())
            self._save_current_profile()
            return True, "Password updated"
        except Exception as e:
            return False, str(e)
