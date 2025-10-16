from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
from models.user_model import User
from models.student_model import Student
from models.subject_model import grade_from_mark

def overall_grade_for(student: Student) -> Optional[str]:
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
        return Admin(id="000000", name=name.strip(), email=email.strip(), password=password.strip(), role="admin")

    # ---------- Queries / transforms over students ----------
    def list_students(self, students: List[Student]) -> List[dict]:
        out: List[dict] = []
        for s in students:
            avg = s.average_mark()
            out.append({
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "subjects_count": len(s.subjects),
                "avg": None if avg is None else round(avg, 2),
                "grade": overall_grade_for(s),
            })
        return out

    def partition_pass_fail(self, students: List[Student]) -> Dict[str, List[Student]]:
        result: Dict[str, List[Student]] = {"PASS": [], "FAIL": []}
        for s in students:
            avg = s.average_mark()
            if avg is None:
                continue
            (result["PASS"] if avg >= 50.0 else result["FAIL"]).append(s)
        return result

    def remove_student_by_id(self, students: List[Student], student_id: str) -> Tuple[List[Student], bool]:
        sid = student_id.strip()
        filtered = [s for s in students if s.id != sid]
        return filtered, len(filtered) != len(students)

    def clear_all_students(self, students: List[Student]) -> List[Student]:
        return []

    def group_by_grade(self, students: List[Student]) -> Dict[str, List[Student]]:
        buckets: Dict[str, List[Student]] = {}
        for s in students:
            g = overall_grade_for(s)
            if g is None:
                continue
            buckets.setdefault(g, []).append(s)
        return buckets