from typing import Optional, Tuple
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
import re

class StudentController:
    def __init__(self, db):
        self.db = db
        self.current_student: Optional[Student] = None

    # --- helpers for validation ---
    def _valid_email(self, email: str) -> bool:
        return (
            email.strip().lower().endswith("@university.com")
            and re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()) is not None
        )

    def _valid_password(self, pw: str) -> bool:
        # Example rule: ≥8 chars, at least one letter + one number
        return len(pw) >= 8 and any(c.isalpha() for c in pw) and any(c.isdigit() for c in pw)

    # --- main login method ---
    def login(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        # 1) Validate formats
        if not self._valid_email(email) or not self._valid_password(password):
            return False, "bad_format"

        # 2) Load students from DB
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)

        # 3) Find matching student
        for s in students:
            if s.email.strip().lower() == email.strip().lower():
                # found → check password
                if s.verify_password(password):
                    self.current_student = s
                    return True, "student"
                else:
                    return False, "bad_password"

        # 4) No student found
        return False, "no_such_user"

    def register(self, name: str, email: str, password: str) -> Tuple[bool, str]:
        raw = self.db.read_from_file()                    # always re-read
        students = students_from_dicts(raw)

        email_norm = email.strip().lower()
        existing = next((s for s in students if s.email.strip().lower() == email_norm), None)
        if existing:
            return False, f"Student {existing.name} already exists"   # exact wording

        # Create and persist (Student.create now stores email in lowercase)
        new_student = Student.create(name, email, password)
        students.append(new_student)

        # keep any non-student records as-is
        others = [d for d in raw if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))
        return True, f"Enrolling Student {new_student.name}"

    
    def validate_credentials(self, email: str, password: str):
        """
        Validate email and password format according to assignment rules.
        Returns (bool, message)
        """
        # Email validation
        if not email.lower().endswith("@university.com"):
            return False, "Incorrect email or password format"

        # Password pattern: Uppercase + at least 5 letters + 3+ digits
        pattern = r"^[A-Z][a-zA-Z]{5,}[0-9]{3,}$"
        if not re.match(pattern, password):
            return False, "Incorrect email or password format"

        return True, "email and password formats acceptable"

    def save_current(self):
        if not self.current_student:
            return
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)
        others = [d for d in raw if d.get("role") != "student"]

        for i, s in enumerate(students):
            if s.email.strip().lower() == self.current_student.email.strip().lower():
                students[i] = self.current_student
                break

        self.db.write_to_file(others + students_to_dicts(students))
        print("[DEBUG][StudentController] Saved current student to DB")

    def enrol_subject(self, title: str) -> Tuple[bool, str]:
        try:
            subject = self.current_student.enrol_subject(title)
            self.save_current()
            return True, f"Enrolled in {subject.title} (ID {subject.id})"
        except Exception as e:
            return False, str(e)

    def remove_subject(self, subject_id: str) -> Tuple[bool, str]:
        removed = self.current_student.remove_subject(subject_id)
        if removed:
            self.save_current()
            return True, f"Removed subject {subject_id}"
        return False, "Subject not found."

    def change_password(self, new_password: str) -> Tuple[bool, str]:
        try:
            self.current_student.change_password(new_password)
            self.save_current()
            return True, "Password updated."
        except Exception as e:
            return False, str(e)

    def logout(self):
        self.current_student = None
