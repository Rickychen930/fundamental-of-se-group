import re
from model.student import Student
from model.database import Database

EMAIL_PATTERN = r"^[\w\.]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

class StudentController:
    @staticmethod
    def register(name, email, password):
        if not re.fullmatch(EMAIL_PATTERN, email):
            return "Invalid email format. Must end with @university.com"

        if not re.fullmatch(PASSWORD_PATTERN, password):
            return ("Invalid password format. Must start with uppercase, "
                    "contain at least 5 letters, and end with 3 or more digits.")

        students = Database.load()
        if any(s.get('email') == email for s in students if isinstance(s, dict)):
            return "Student already exists."

        student = Student(name, email, password)
        students.append(student.to_dict())
        Database.save(students)
        return f"Registered successfully with ID {student.id}"

    @staticmethod
    def login(email, password):
        students = Database.load()
        for s in students:
            if isinstance(s, dict) and s.get('email') == email and s.get('password') == password:
                return Student.from_dict(s)
        return None

    @staticmethod
    def update(student):
        students = Database.load()
        for i, s in enumerate(students):
            if isinstance(s, dict) and s.get('id') == student.id:
                students[i] = student.to_dict()
                break
        Database.save(students)
