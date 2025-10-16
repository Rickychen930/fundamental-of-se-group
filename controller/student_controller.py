from typing import Optional, Tuple
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
import re

class StudentController:
    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    def login(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)
        for student in students:
            if student.email.strip().lower() == email.strip().lower() and student.verify_password(password):
                print(f"[DEBUG][StudentController] Login success for {email}")
                self.current_student = student
                return True, "student"
        print(f"[DEBUG][StudentController] Login failed for {email}")
        return False, None

    def register(self, name: str, email: str, password: str):
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)

        if any(s.email.strip().lower() == email.strip().lower() for s in students):
            return False, f"Student {name} already exists."

        new_student = Student.create(name, email, password)
        students.append(new_student)

        others = [d for d in raw if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))

        return True, f"Student {new_student.name} registered successfully"

    
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
