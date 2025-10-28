from __future__ import annotations
from dataclasses import dataclass
import random

GRADE_ORDER = ["HD", "D", "C", "P", "F"]  # explicit order for Grade Grouping

def gen_subject_id() -> str:
    return f"{random.randint(1, 999):03d}"

def grade_from_mark(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "F"

@dataclass
class Subject:
    id: str
    title: str
    mark: int
    grade: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "mark": self.mark,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data: dict) -> Subject:
        return Subject(
            id=data["id"],
            title=data["title"],
            mark=data["mark"],
            grade=data["grade"]
        )
