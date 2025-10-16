from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import re, random

Role = Literal["student", "admin"]
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@university\.com$")
PWD_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")

def gen_student_id() -> str:
    return f"{random.randint(1, 999_999):06d}"

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    role: Role = "student"

    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(EMAIL_RE.match(email.strip()))

    @staticmethod
    def validate_password(password: str) -> bool:
        return bool(PWD_RE.match(password.strip()))

    def verify_password(self, password: str) -> bool:
        return self.password == password.strip()

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_student(self) -> bool:
        return self.role == "student"
