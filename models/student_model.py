from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import random

from models.user_model import User, gen_student_id
from models.subject_model import Subject, gen_subject_id, grade_from_mark

MAX_SUBJECTS = 4

@dataclass
class Student(User):
    subjects: List[Subject] = field(default_factory=list)

    @staticmethod
    def create(name: str, email: str, password: str) -> "Student":
        # Delegate format rules to User validators (single source of truth)
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        if not User.validate_password(password):
            raise ValueError("Password must start with an uppercase, have ≥5 letters, then ≥3 digits.")
        return Student(
            id=gen_student_id(),
            name=name.strip(),
            email=email.strip().lower(),   # normalize for uniqueness
            password=password.strip(),
            role="student",
            subjects=[]
        )

    # --- Domain rules live in the model ---
    def enrol_subject(self, title: str) -> Subject:
        if len(self.subjects) >= MAX_SUBJECTS:
            raise ValueError("Cannot enrol in more than four (4) subjects.")
        norm_title = title.strip()
        if not norm_title:
            raise ValueError("Subject title cannot be empty.")
        if any(s.title.lower() == norm_title.lower() for s in self.subjects):
            raise ValueError("Subject already enrolled.")
        mark = random.randint(25, 100)
        sub = Subject(id=gen_subject_id(), title=norm_title, mark=mark, grade=grade_from_mark(mark))
        self.subjects.append(sub)
        return sub

    def remove_subject(self, subject_id: str) -> bool:
        sid = subject_id.strip()
        for i, s in enumerate(self.subjects):
            if s.id == sid:
                del self.subjects[i]
                return True
        return False

    def change_password(self, new_password: str) -> None:
        if not User.validate_password(new_password):
            raise ValueError("Password must start with an uppercase, have ≥5 letters, then ≥3 digits.")
        self.password = new_password.strip()

    def average_mark(self) -> Optional[float]:
        if not self.subjects:
            return None
        return sum(subj.mark for subj in self.subjects) / len(self.subjects)

    def has_passed(self) -> bool:
        avg = self.average_mark()
        return bool(avg is not None and avg >= 50.0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "subjects": [s.to_dict() for s in self.subjects]
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        return Student(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role=data.get("role", "student"),
            subjects=[Subject.from_dict(s) for s in data.get("subjects", [])]
        )

def students_from_dicts(data: list[dict]) -> list["Student"]:
    return [Student.from_dict(d) for d in data if d.get("role") == "student"]

def students_to_dicts(students: list["Student"]) -> list[dict]:
    return [s.to_dict() for s in students]