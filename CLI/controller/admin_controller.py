from model.database import Database
from model.student import Student

class AdminController:
    @staticmethod
    def show_all():
        return AdminController._load_students()

    @staticmethod
    def remove_student(student_id):
        students = AdminController._load_students()
        filtered = [s for s in students if s.id != student_id]
        Database.save([s.to_dict() for s in filtered])

    @staticmethod
    def partition():
        students = AdminController._load_students()
        return [(s.name, "PASS" if s.average_mark >= 50 else "FAIL") for s in students]

    @staticmethod
    def group_by_grade():
        students = AdminController._load_students()
        grades = {}
        for s in students:
            for subj in s.enrolled_subjects:
                grades.setdefault(subj.grade, []).append(s.name)
        return grades

    @staticmethod
    def clear():
        Database.clear()

    @staticmethod
    def _load_students():
        raw = Database.load()
        return [Student.from_dict(s) for s in raw if isinstance(s, dict)]
