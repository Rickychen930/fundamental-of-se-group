from __future__ import annotations
from view.CLI.base_page import BasePage
from controller.subject_controller import SubjectController
from db.database import Database

class StudentPage(BasePage):
    """
    Pure CLI: owns input()/print() and presentation.
    """
    def __init__(self, controller):
        self.db = Database()
        self.controller = controller
        self.subjects = SubjectController(self.db)

    def show(self):
        while True:
            print("\t\033[96mStudent System (l/r/x) : ", end="")
            student_choice = input().strip().lower()

            if student_choice == 'r':
                self.register()
            elif student_choice == 'l':
                self.login()
            elif student_choice == 'x':
                break
            else:
                continue

    def register(self):
        print("\t\033[92mStudent Sign Up\033[0m")

        # 1) Loop until email/password format is acceptable (controller uses model validators)
        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()

            ok, msg = self._validate_formats(email, password)
            if not ok:
                print(f"\t\033[91m{msg}\033[0m")
                continue

            print(f"\t\033[93memail and password formats acceptable\033[0m")
            break

        name = input("\tName: ").strip()
        if not name:
            print("\t\033[91mName cannot be empty.\033[0m")
            return

        ok, msg = self.controller.register(name, email, password)
        color = "\033[92m" if ok else "\033[91m"
        print(f"\t{color}{msg}\033[0m")

    def login(self):
        print("\t\033[92mStudent Sign In\033[0m")
        email = input("\tEmail: ").strip()
        password = input("\tPassword: ").strip()

        success, reason = self.controller.login(email, password)

        if success:
            print("\t\033[93memail and password formats acceptable\033[0m")
            self.subjects.set_current_student(self.controller.current_student)
            self.subject_menu()
            return

        if reason == "bad_format":
            print("\t\033[91mIncorrect email or password format\033[0m")
        elif reason == "no_such_user":
            print("\t\033[93memail and password formats acceptable\033[0m")
            print("\t\033[91mStudent does not exist\033[0m")
        elif reason == "bad_password":
            print("\t\033[93memail and password formats acceptable\033[0m")
            print("\t\033[91mIncorrect password\033[0m")
        else:
            print("\t\033[91mInvalid credentials.\033[0m")

    # --- Subject submenu & flows ---
    def subject_menu(self):
        student = self.controller.current_student
        while True:
            choice = input("\t\033[96mStudent Course Menu (c/e/r/s/x): \033[0m").strip().lower()
            if choice == "c":
                self.change_password(student)
            elif choice == "e":
                self._enrol_subject_flow(student)
            elif choice == "r":
                self._remove_subject_flow(student)
            elif choice == "s":
                self._show_subjects_flow(student)
            elif choice == "x":
                break
            else:
                continue

    def _enrol_subject_flow(self, student):
        ok, msg, sub = self.subjects.enrol_auto()  # returns (ok, msg, Subject|None)
        if ok and sub:
            print(f"\t\033[93mEnrolling in {sub.title}-{sub.id}")
            print(f"\t\033[93mYou are now enrolled in {len(self.subjects.list_subjects())} out of 4 subjects")
        else:
            print(f"\t\033[91m{msg}\033[0m")

    def _show_subjects_flow(self, student):
        items = self.subjects.list_subjects()
        print(f"\t\033[93mShowing {len(items)} subject{'s' if len(items)!=1 else ''}\033[0m")
        for s in items:
            print(f"\t[  {s.title}  -- mark = {s.mark} -- grade =  {s.grade}  ]")

    def _remove_subject_flow(self, student):
        items = self.subjects.list_subjects()
        if not items:
            print("\t\033[93mNo subjects to remove.\033[0m")
            return
        for s in items:
            print(f"\t[ id={s.id}  title={s.title}  mark={s.mark}  grade={s.grade} ]")
        sid = input("\tRemove Subject by ID: ").strip()
        print(f"\t\033[93mDropping {sid}")
        ok, msg = self.subjects.remove_by_id(sid)
        print(f"\t{'\033[93m' if ok else '\033[91m'}{msg}\033[0m")

    def change_password(self, student):
        print("\t\033[96mUpdating Password\033[0m")

        while True:
            new_pwd = input("\tNew Password: ").strip()
            confirm = input("\tConfirm Password: ").strip()

            ok, msg = self.subjects.change_password(new_pwd, confirm)
            color = "\033[93m" if ok else "\033[91m"
            print(f"\t{color}{msg}\033[0m")

            if ok:
                break  # password updated successfully
            else:
                continue

    def show_average(self, student):
        avg = self.subjects.average()
        if avg is None:
            print("\t\033[93mNo subjects yet; average unavailable.\033[0m")
        else:
            print(f"\tAverage mark = {avg:.2f}")

    # --- private helpers ---
    def _validate_formats(self, email: str, password: str) -> tuple[bool, str]:
        # Ask controller.login to evaluate using model validators without side-effects
        # We replicate the messages expected by the transcript.
        from models.user_model import User
        if not User.validate_email(email) or not User.validate_password(password):
            return False, "Incorrect email or password format"
        return True, "OK"