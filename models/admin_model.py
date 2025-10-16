from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from models.user_model import User
from models.student_model import Student
from models.subject_model import grade_from_mark

def overall_grade_for(student: Student) -> str:
    avg = int(round(student.average_mark()))
    return grade_from_mark(avg)

@dataclass
class Admin(User):
    @staticmethod
    def create(name: str, email: str, password: str) -> Admin:
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        return Admin(id="000000", name=name.strip(), email=email.strip(),
                     password=password.strip(), role="admin")

    def list_students(self, students: List[Student]) -> List[dict]:
        return [{
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "subjects_count": len(s.subjects),
            "avg": round(s.average_mark(), 2),
            "grade": overall_grade_for(s)
        } for s in students]

    def group_by_grade(self, students: List[Student]) -> dict:
        buckets = {"HD": [], "D": [], "C": [], "P": [], "Z": []}
        for s in students:
            grade = overall_grade_for(s)
            buckets[grade].append(s)
        return buckets

    def partition_pass_fail(self, students: List[Student]) -> dict:
        result = {"PASS": [], "FAIL": []}
        for s in students:
            key = "PASS" if s.has_passed() else "FAIL"
            result[key].append(s)
        return result

    def remove_student_by_id(self, students: List[Student], student_id: str) -> Tuple[List[Student], bool]:
        sid = student_id.strip()
        filtered = [s for s in students if s.id != sid]
        removed = len(filtered) != len(students)
        return filtered, removed

    def clear_all_students(self, students: List[Student]) -> List[Student]:
        return []
