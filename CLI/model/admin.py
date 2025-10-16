import random
from model.user import User

class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.id = f"A{random.randint(1, 9999):04d}"

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "id": self.id,
            "role": "admin"
        })
        return base

    @staticmethod
    def from_dict(data):
        admin = Admin(data['name'], data['email'], data['password'])
        admin.id = data['id']
        return admin
