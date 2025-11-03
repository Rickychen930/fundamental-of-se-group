from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
from models.user_model import User
from models.student_model import Student
from models.subject_model import grade_from_mark

def overall_grade_for(student: Student) -> Optional[str]:
    """
    Compute the overall grade (HD, D, C, P, F) for a given student.

    Returns:
        str: grade letter corresponding to the student's average.
        None: if the student has no subjects or marks.
    """
    avg = student.average_mark()
    if avg is None:
        return None
    return grade_from_mark(int(round(avg)))


@dataclass
class Admin(User):
    """
    Administrator utilities.

    NOTE: All operations below are static and do not require an Admin instance.
    """

    # Keeping create() is optional; the controller no longer needs an instance.
    @staticmethod
    def create(name: str, email: str, password: str) -> "Admin":
        """
        Create a new Admin instance with basic validation.
        Useful if you still want a material Admin somewhere (not required).
        """
        if not User.validate_email(email):
            raise ValueError("Email must end with @university.com.")
        return Admin(
            id="000000",
            name=name.strip(),
            email=email.strip(),
            password=password.strip(),
        )

    # ---------- Queries / transforms over students (static) ----------

    @staticmethod
    def list_students(students: List[Student]) -> List[dict]:
        """
        Return a list of students with their key summary information.

        Each record includes:
          - id, name, email
          - number of enrolled subjects
          - average mark
          - overall grade
        """
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

    @staticmethod
    def partition_pass_fail(students: List[Student]) -> Dict[str, List[Student]]:
        """
        Separate students into PASS and FAIL groups based on their average mark.

        Returns:
            dict: {"PASS": [...], "FAIL": [...]}
        """
        result: Dict[str, List[Student]] = {"PASS": [], "FAIL": []}
        for s in students:
            avg = s.average_mark()
            if avg is None:
                continue
            (result["PASS"] if avg >= 50.0 else result["FAIL"]).append(s)
        return result

    @staticmethod
    def remove_student_by_id(students: List[Student], student_id: str) -> Tuple[List[Student], bool]:
        """
        Remove a student from the list by their unique ID.

        Returns:
            (updated_list, removed_flag)
            removed_flag is True if a student was actually removed.
        """
        sid = student_id.strip()
        filtered = [s for s in students if s.id != sid]
        return filtered, len(filtered) != len(students)

    @staticmethod
    def clear_all_students(students: List[Student]) -> List[Student]:
        """
        Clear all student records. Returns an empty list.
        """
        return []

    @staticmethod
    def group_by_grade(students: List[Student]) -> Dict[str, List[Student]]:
        """
        Group students by their overall grade (HD, D, C, P, F).

        Returns:
            dict: grade → list of students
        """
        buckets: Dict[str, List[Student]] = {}
        for s in students:
            g = overall_grade_for(s)
            if g is None:
                continue
            buckets.setdefault(g, []).append(s)
        return buckets
