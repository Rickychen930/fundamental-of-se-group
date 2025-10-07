class RegisterViewModel:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.confirm_password = ""
        self.email = ""

    def set_credentials(self, username: str, password: str, confirm_password: str, email: str = ""):
        self.username = username.strip()
        self.password = password.strip()
        self.confirm_password = confirm_password.strip()
        self.email = email.strip()

    def validate_inputs(self):
        """Validate user input before registration"""
        if not self.username:
            return False, "Username cannot be empty."
        if not self.email or "@" not in self.email:
            return False, "Invalid email address."
        if not self.password:
            return False, "Password cannot be empty."
        if len(self.password) < 6:
            return False, "Password must be at least 6 characters long."
        if self.password != self.confirm_password:
            return False, "Password confirmation does not match."
        return True, "Input is valid."

    def register(self):
        """
        Simulate registration process.
        This is where you would connect to a database, API, or other service.
        """
        is_valid, message = self.validate_inputs()
        if not is_valid:
            return False, message

        # TODO: Integrate with backend or database
        # Example: check if username already exists, then save new user
        # For now, return dummy success
        return True, f"Registration successful. Welcome, {self.username}!"
