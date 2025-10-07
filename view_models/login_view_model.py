class LoginViewModel:
    def __init__(self):
        self.username = ""
        self.password = ""

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def validate_credentials(self):
        # Contoh validasi sederhana
        if not self.username or not self.password:
            return False, "Username dan password tidak boleh kosong."

        if len(self.username) < 3:
            return False, "Username terlalu pendek."

        if len(self.password) < 6:
            return False, "Password harus minimal 6 karakter."

        return True, "Validasi berhasil."

    def login(self):
        # Simulasi proses login
        if self.username == "admin" and self.password == "admin123":
            return True, "Login berhasil."
        else:
            return False, "Username atau password salah."
