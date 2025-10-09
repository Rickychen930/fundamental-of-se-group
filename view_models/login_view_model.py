class LoginViewModel:
    def __init__(self):
        self.username = ""
        self.password = ""

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def validate_credentials(self):
        if not self.username or not self.password:
            return False, "Username and password cannot be empty."
        if len(self.username) < 3:
            return False, "Username is too short."
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, "Validation successful."

    def login(self):
        if self.username == "admin" and self.password == "admin123":
            return True, "Login successful."
        return False, "Incorrect username or password."
