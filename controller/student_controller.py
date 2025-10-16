from __future__ import annotations
from typing import Optional, Tuple
from db.database import Database
from models.student_model import Student, students_from_dicts, students_to_dicts
from models.user_model import User  # use central validators

class StudentController:
    """
    Orchestrates student flows. No prints. No regex/business rules here.
    """
    def __init__(self, db: Database):
        self.db = db
        self.current_student: Optional[Student] = None

    # --- main login method ---
    def login(self, email: str, password: str) -> tuple[bool, Optional[str]]:
        # Validate formats via User validators (keeps rules out of controller)
        if not (User.validate_email(email) and User.validate_password(password)):
            return False, "bad_format"

        raw = self.db.read_from_file()
        students = students_from_dicts(raw)

        email_norm = email.strip().lower()
        for s in students:
            if s.email.strip().lower() == email_norm:
                if s.verify_password(password):
                    self.current_student = s
                    return True, "student"
                else:
                    return False, "bad_password"
        return False, "no_such_user"

    def register(self, name: str, email: str, password: str) -> tuple[bool, str]:
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)

        email_norm = email.strip().lower()
        if any(s.email.strip().lower() == email_norm for s in students):
            # Match expected message shape from your page/transcripts
            return False, f"Student {name.strip()} already exists"

        # Delegate validation & creation to the model
        new_student = Student.create(name, email, password)
        students.append(new_student)

        others = [d for d in raw if d.get("role") != "student"]
        self.db.write_to_file(others + students_to_dicts(students))
        return True, f"Enrolling Student {new_student.name}"

    def save_current(self) -> None:
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

    # Convenience methods used by some pages (flows)
    def enrol_subject(self, title: str) -> tuple[bool, str]:
        try:
            subject = self.current_student.enrol_subject(title)
            self.save_current()
            return True, f"Enrolled in {subject.title} (ID {subject.id})"
        except Exception as e:
            return False, str(e)

    def remove_subject(self, subject_id: str) -> tuple[bool, str]:
        removed = self.current_student.remove_subject(subject_id)
        if removed:
            self.save_current()
            return True, f"Removed subject {subject_id}"
        return False, "Subject not found."

    def change_password(self, new_password: str) -> tuple[bool, str]:
        try:
            self.current_student.change_password(new_password)
            self.save_current()
            return True, "Password updated."
        except Exception as e:
            return False, str(e)

    def logout(self) -> None:
        self.current_student = None