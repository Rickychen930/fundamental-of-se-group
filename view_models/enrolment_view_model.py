# Enrolment logic for the Dashboard page

import random
import re
from typing import Tuple, List, Dict, Optional


try:
    from models.user_model import UserModel
except Exception:
    UserModel = object 

# Password rule: Capital + >=5 letters + >=3 digits
PASSWORD_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")


class EnrolmentViewModel:
    

    # Max subjects a student can enrol in
    MAX_SUBJECTS = 4

    def __init__(self):
        self.user: Optional[UserModel] = None

    def set_user(self, user: "UserModel") -> None:
        # Attach the currently logged-in user.
        self.user = user
        if not hasattr(self.user, "subjects") or self.user.subjects is None:
            self.user.subjects: List[Dict] = []

    # update password
    def change_password(self, new_pwd: str) -> Tuple[bool, str]:
        if not self.user:
            return False, "No user session found."
        if not new_pwd:
            return False, "Password cannot be empty."
        if not PASSWORD_RE.match(new_pwd):
            return False, "Must start with a capital, then >=5 letters and >=3 digits."
        self.user.password = new_pwd
        
        return True, "Password updated successfully."

    # add a subject (id = random 3-digit 001..999)
    def enrol(self, subject_title: str = "") -> Tuple[bool, Dict]:
        if not self.user:
            return False, {"message": "No user session found."}

        # Limit to MAX_SUBJECTS
        if len(self.user.subjects) >= self.MAX_SUBJECTS:
            return False, {"message": "You cannot enrol in more than 4 subjects."}

        clean_title = (subject_title or "").strip() or "Untitled"

        # prevent duplicate title for the same student
        if any(s["title"] == clean_title for s in self.user.subjects):
            return False, {"message": "You already enrolled in this subject."}

        # Generate a unique random 3-digit id (001..999) within the student's list
        existing_ids = {s["id"] for s in self.user.subjects}
        sid = None
        for _ in range(2000):  # simple safety loop  
            candidate = f"{random.randint(1, 999):03d}"  # "007", "123", "999"
            if candidate not in existing_ids:
                sid = candidate
                break
        if sid is None:
            return False, {"message": "Cannot generate subject id. Please try again."}

        subject = {
            "id": sid,
            "title": clean_title,
        }

        self.user.subjects.append(subject)
        # persist if needed
        return True, subject

    # delete a subject by id (3-digit string)
    def remove(self, subject_id: str) -> Tuple[bool, str]:
        if not self.user:
            return False, "No user session found."
        before = len(self.user.subjects)
        self.user.subjects = [s for s in self.user.subjects if s["id"] != subject_id]
        removed = len(self.user.subjects) < before
        return removed, ("Subject removed." if removed else "Subject not found.")

    # list all subjects (id + title only)
    def list_subjects(self) -> List[Dict]:
        if not self.user:
            return []
        return list(self.user.subjects)
