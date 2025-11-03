from __future__ import annotations
from dataclasses import dataclass
import random

# Grade order used for admin grade grouping and reporting
GRADE_ORDER = ["HD", "D", "C", "P", "F"]

# The maximum number of subjects a student can enrol in
MAX_SUBJECTS = 4


def gen_subject_id() -> str:
    """
    Generate a random 3-digit subject ID (001–999) as a zero-padded string.
    Example: "007", "418", "999"
    """
    return f"{random.randint(1, 999):03d}"


def grade_from_mark(mark: int) -> str:
    """
    Convert a numeric mark (0–100) into a grade letter:
        HD: ≥85
        D : ≥75
        C : ≥65
        P : ≥50
        F : <50
    """
    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "D"
    if mark >= 65:
        return "C"
    if mark >= 50:
        return "P"
    return "F"

@dataclass
class Subject:
    """
    Represents a subject enrolment with its unique ID, title, mark, and grade.
    Instances are usually created through Student.enrol_subject().
    """
    id: str       # 3-digit subject ID, e.g. "123"
    title: str    # Human-readable title, e.g. "Subject-123"
    mark: int     # Randomly assigned numeric mark, 0–100
    grade: str    # Grade ("HD", "D", "C", "P", "F")


    def to_dict(self) -> dict:
        """
        Convert this Subject into a dictionary suitable for JSON/DB storage.
        """
        return {
            "id": self.id,
            "title": self.title,
            "mark": self.mark,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data: dict) -> Subject:
        """
        Reconstruct a Subject instance from its dictionary form.
        Expected keys: id, title, mark, grade
        """
        return Subject(
            id=data["id"],
            title=data["title"],
            mark=data["mark"],
            grade=data["grade"]
        )
