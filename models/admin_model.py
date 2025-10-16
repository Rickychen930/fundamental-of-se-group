from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple

from models.user_model import User
from models.student_model import Student
from models.subject_model import grade_from_mark


# --- SINGLE, SAFE, MODULE-LEVEL FUNCTION (this is what controllers import) ---
def overall_grade_for(student: Student) -> Optional[str]:
    """
    Returns a grade code based on the student's overall average, or None
    if the student has no subjects/marks yet.
    """
    avg = student.average_mark()
    if avg is None:
        return None
    return grade_from_mark(int(round(avg)))


@dataclass
class Admin(User):
    @staticmethod
    def create(name: str, email: str, password: str) -> "Admin":
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        return Admin(
            id="000000",
            name=name.strip(),
            email=email.strip(),
            password=password.strip(),
            role="admin",
        )

    def list_students(self, students: List[Student]) -> List[dict]:
        result = []
        for s in students:
            avg = s.average_mark()  # may be None
            result.append({
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "subjects_count": len(s.subjects),
                "avg": None if avg is None else round(avg, 2),
                "grade": overall_grade_for(s),  # safe
            })
        return result

    def partition_pass_fail(self, students: list[Student]) -> dict:
        result = {"PASS": [], "FAIL": []}
        for s in students:
            avg = s.average_mark()
            if avg is None:
                continue  # <- don't count unenrolled/unassessed students
            if avg >= 50.0:
                result["PASS"].append(s)
            else:
                result["FAIL"].append(s)
        return result


    def remove_student_by_id(self, students: List[Student], student_id: str) -> Tuple[List[Student], bool]:
        sid = student_id.strip()
        filtered = [s for s in students if s.id != sid]
        removed = len(filtered) != len(students)
        return filtered, removed

    def clear_all_students(self, students: List[Student]) -> List[Student]:
        return []
