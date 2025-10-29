# -------------------------------------------------------------------
# Student Model
# -------------------------------------------------------------------

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import random
from models.user_model import User, gen_student_id
from models.subject_model import Subject, gen_subject_id, grade_from_mark, MAX_SUBJECTS

@dataclass
class Student(User):
    """
    Represents a student user in the system.

    Inherits from `User` and extends it with subject enrolment
    management. Each student may enrol in up to MAX_SUBJECTS subjects.
    """

    subjects: List[Subject] = field(default_factory=list)

    @staticmethod
    def create(name: str, email: str, password: str) -> "Student":
        """
        Create a new Student instance after validating email and password.

        Validation rules come from User validators to ensure consistency:
          - Email must end with '@university.com'
          - Password must start with uppercase, include ≥5 letters, and ≥3 digits
        """
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        if not User.validate_password(password):
            raise ValueError("Password must start with an uppercase, have ≥5 letters, then ≥3 digits.")

        return Student(
            id=gen_student_id(),
            name=name.strip(),
            email=email.strip().lower(),   # normalize for uniqueness
            password=password.strip(),
            subjects=[]
        )

    def enrol_subject(self, title: str) -> Subject:
        """
        Enrol the student in a new subject.

        A random subject ID is generated, and the title is standardized
        as 'Subject-<id>' to match CLI output format.

        Raises:
            ValueError: if the student already has MAX_SUBJECTS or if
                        the randomly generated subject ID is duplicated.
        """
        if len(self.subjects) >= MAX_SUBJECTS:
            raise ValueError(f"students are allowed to enrol in {MAX_SUBJECTS} subjects only")

        new_id = gen_subject_id()
        norm_title = f"Subject-{new_id}"

        # Prevent duplicate enrolments by ID
        if any(s.id == new_id for s in self.subjects):
            raise ValueError("Subject already enrolled.")

        # Randomly assign a mark (25–100) and calculate grade
        mark = random.randint(25, 100)
        sub = Subject(id=new_id, title=norm_title, mark=mark, grade=grade_from_mark(mark))
        self.subjects.append(sub)
        return sub

    def remove_subject(self, subject_id: str) -> bool:
        """
        Remove a subject from the student's enrolment list by ID.

        Returns:
            True if the subject was found and removed, False otherwise.
        """
        sid = subject_id.strip()
        for i, s in enumerate(self.subjects):
            if s.id == sid:
                del self.subjects[i]
                return True
        return False

    def change_password(self, new_password: str) -> None:
        """
        Update the student's password, validating the format.

        Raises:
            ValueError: if the new password does not meet format rules.
        """
        if not User.validate_password(new_password):
            raise ValueError("Incorrect password format")
        self.password = new_password.strip()

    def average_mark(self) -> Optional[float]:
        """
        Compute the student's average mark across all enrolled subjects.

        Returns:
            The average (float) or None if the student has no subjects.
        """
        if not self.subjects:
            return None
        return sum(subj.mark for subj in self.subjects if subj.mark is not None) / len(self.subjects)

    def has_passed(self) -> bool:
        """
        Determine whether the student has passed overall.

        A student is considered to have passed if their average mark ≥ 50.
        """
        avg = self.average_mark()
        return bool(avg is not None and avg >= 50.0)

    def to_dict(self) -> dict:
        """
        Convert this Student into a dictionary suitable for JSON/DB storage.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [s.to_dict() for s in self.subjects]
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        """
        Rebuild a Student instance from its dictionary form.
        Used when loading from the database file.
        """
        return Student(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            subjects=[Subject.from_dict(s) for s in data.get("subjects", [])]
        )


def students_from_dicts(data: list[dict]) -> list["Student"]:
    """Convert a list of student dictionaries into Student objects."""
    return [Student.from_dict(d) for d in data]


def students_to_dicts(students: list["Student"]) -> list[dict]:
    """Convert a list of Student objects into dictionaries for storage."""
    return [s.to_dict() for s in students]
