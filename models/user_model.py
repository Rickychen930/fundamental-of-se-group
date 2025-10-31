# -------------------------------------------------------------------
# User Model
# -------------------------------------------------------------------

from __future__ import annotations
from dataclasses import dataclass
import re, random


# Valid university email format (must end with @university.com)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@university\.com$")

# Password format:
#   - Starts with an uppercase letter
#   - Followed by at least 5 letters
#   - Ends with at least 3 digits
# Example: Helloworld123
PWD_RE = re.compile(r"^[A-Z][A-Za-z]{5,}\d{3,}$")


def gen_student_id() -> str:
    """
    Generate a 6-digit student ID as a zero-padded string.
    Example: "000123", "457890"
    """
    return f"{random.randint(1, 999_999):06d}"


@dataclass
class User:
    """
    Base class representing a generic user of the system.
    This class is extended by both `Student` and `Admin`.

    Attributes:
        id: Unique numeric ID as a string (e.g., "000123")
        name: Full name of the user
        email: Must end with '@university.com'
        password: As above for format
    """

    id: str
    name: str
    email: str
    password: str

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Check if the provided email is in a valid university format.

        Returns:
            True if valid, False otherwise.
        """
        return bool(EMAIL_RE.match(email.strip()))

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate that the password meets system complexity requirements.

        Must:
          - Start with an uppercase letter
          - Have ≥5 letters after that
          - End with ≥3 digits
        """
        return bool(PWD_RE.match(password.strip()))

    def verify_password(self, password: str) -> bool:
        """
        Verify that the provided password matches the stored one.

        Returns:
            True if the password matches, False otherwise.
        """
        return self.password == password.strip()
