import random
from model.user import User
from model.subject import Subject

class Student(User):
    MAX_SUBJECTS = 4

    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.id = f"{random.randint(1, 999999):06d}"
        self.enrolled_subjects = []
        self.average_mark = 0.0

    def enrol_subject(self):
        if len(self.enrolled_subjects) >= Student.MAX_SUBJECTS:
            return "Max 4 subjects allowed."
        subject = Subject()
        self.enrolled_subjects.append(subject)
        self.update_average_mark()
        return f"Enrolled in {subject.id} with mark {subject.mark} and grade {subject.grade}"

    def remove_subject(self, subject_id):
        original_count = len(self.enrolled_subjects)
        self.enrolled_subjects = [s for s in self.enrolled_subjects if s.id != subject_id]
        self.update_average_mark()
        if len(self.enrolled_subjects) == original_count:
            return f"No subject found with ID {subject_id}."
        return f"Subject {subject_id} removed."

    def update_average_mark(self):
        if self.enrolled_subjects:
            total = sum(s.mark for s in self.enrolled_subjects)
            self.average_mark = total / len(self.enrolled_subjects)
        else:
            self.average_mark = 0.0

    def show_subjects(self):
        if not self.enrolled_subjects:
            return "No subjects enrolled."
        return "\n".join(
            f"[ Subject:{s.id} --- mark = {s.mark} --- grade = {s.grade} ]"
            for s in self.enrolled_subjects
        )

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "id": self.id,
            "role": "student",
            "subjects": [s.to_dict() for s in self.enrolled_subjects],
            "average_mark": self.average_mark
        })
        return base

    @staticmethod
    def from_dict(data):
        student = Student(data['name'], data['email'], data['password'])
        student.id = data['id']
        subject_dicts = data.get('subjects', [])
        student.enrolled_subjects = [Subject.from_dict(s) for s in subject_dicts if isinstance(s, dict)]
        student.update_average_mark()
        return student
