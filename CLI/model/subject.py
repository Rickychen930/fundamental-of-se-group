import random

class Subject:
    def __init__(self, id=None, mark=None, grade=None):
        self.id = id or f"{random.randint(1, 999):03d}"
        self.mark = mark if mark is not None else random.randint(25, 100)
        self.grade = grade or self.calculate_grade()

    def calculate_grade(self):
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'F'

    def to_dict(self):
        return {
            "id": self.id,
            "mark": self.mark,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data):
        return Subject(
            id=data.get("id"),
            mark=data.get("mark"),
            grade=data.get("grade")
        )
