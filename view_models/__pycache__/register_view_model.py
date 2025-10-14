# view_models/register_view_model.py

import re

class RegisterViewModel:
    def __init__(self):
        self.username = ""
        self.email = ""
        self.password = ""

    def set_data(self, username, email, password):
        self.username = username.strip()
        self.email = email.strip()
        self.password = password.strip()

    def validate(self):
        if not self.username or not self.email or not self.password:
            return False, "Semua field harus diisi."

        if len(self.username) < 3:
            return False, "Username minimal 3 karakter."

        if not self._is_valid_email(self.email):
            return False, "Format email tidak valid."

        if len(self.password) < 6:
            return False, "Password minimal 6 karakter."

        return True, "Validasi berhasil."

    def register(self):
        # Simulasi proses registrasi
        # Di sini kamu bisa integrasikan dengan database atau API
        print(f"Registrasi: {self.username}, {self.email}")
        return True, "Registrasi berhasil."

    def _is_valid_email(self, email):
        # Validasi email sederhana
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
