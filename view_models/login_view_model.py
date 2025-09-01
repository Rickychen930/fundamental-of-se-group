from models.user_model import UserModel

class LoginViewModel:
    def __init__(self):
        self.user = UserModel()

    def set_username(self, username):
        self.user.username = username

    def set_password(self, password):
        self.user.password = password

    def validate(self):
        return self.user.is_valid()

    def login(self):
        if self.validate():
            print(f"Logging in as {self.user.username}")
            return True
        else:
            print("Invalid credentials")
            return False
