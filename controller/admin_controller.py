from db.database import Database
from models.admin_model import Admin, overall_grade_for
from models.student_model import Student, students_from_dicts, students_to_dicts

class AdminController:
    def __init__(self, db: Database):
        self.db = db
        self.admin = Admin.create("System Admin", "admin@university.com", "AdminPass123")

    def login(self, email: str, password: str):
        if email.strip().lower() == "admin@university.com" and self.admin.verify_password(password):
            print("[DEBUG][AdminController] Admin login success")
            return True, "admin"
        print("[DEBUG][AdminController] Admin login failed")
        return False, None

    def list_students(self):
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)
        return self.admin.list_students(students)

    def group_by_grade(self):
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)

        buckets: dict[str, list[Student]] = {}
        for s in students:
            grade = overall_grade_for(s)   # may be None now
            if grade is None:
                continue                   # skip students with no subjects
            buckets.setdefault(grade, []).append(s)

        return buckets


    def partition_pass_fail(self):
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)
        return self.admin.partition_pass_fail(students)

    def remove_student_by_id(self, student_id: str):
        raw = self.db.read_from_file()
        students = students_from_dicts(raw)
        updated_students, removed = self.admin.remove_student_by_id(students, student_id)
        if removed:
            # Preserve non-student records
            others = [d for d in raw if d.get("role") != "student"]
            self.db.write_to_file(others + students_to_dicts(updated_students))
        return removed

    def clear_all_students(self):
        """Remove all student records from the data file."""
        self.db.clear_all()
        return True
