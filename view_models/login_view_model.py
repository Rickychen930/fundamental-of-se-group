class LoginViewModel:
    def __init__(self):
        self.username = ""
        self.password = ""
        self._user_store = {}  # Injected externally

    def set_credentials(self, username, password):
        self.username = username.strip()
        self.password = password.strip()

    def validate_credentials(self):
        if not self.username or not self.password:
            return False, "Username and password cannot be empty."

    def login(self):
        if not self._user_store:
            return False, "No user data loaded."

        stored_password = self._user_store.get(self.username)
        if stored_password and stored_password == self.password:
            return True, "Login successful."
        return False, "Incorrect username or password."

    def load_users(self, user_dict):
        """
        Injects user data from any source.
        Expected format: { "username1": "password1", "username2": "password2", ... }
        """
        if isinstance(user_dict, dict):
            self._user_store = {
                str(k).strip(): str(v).strip()
                for k, v in user_dict.items()
                if k and v
            }
