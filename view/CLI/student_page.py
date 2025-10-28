from __future__ import annotations
from view.CLI.base_page import BasePage


class StudentPage(BasePage):
    """CLI interface for student registration, login, and subject management."""

    def __init__(self, controller):
        """Use the injected StudentController only."""
        self.controller = controller

    def show(self):
        """Main student menu loop."""
        while True:
            print("\t\033[96mStudent System (l/r/x) : \033[0m", end="")
            student_choice = input().strip().lower()

            if student_choice == 'r':      # Register
                self.register()
            elif student_choice == 'l':    # Login
                self.login()
            elif student_choice == 'x':    # Exit
                break
            else:
                continue

    # ---------- Student registration & login ----------

    def register(self):
        """Handle student registration flow."""
        print("\t\033[92mStudent Sign Up\033[0m")

        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()

            ok, msg = self._validate_formats(email, password)
            if not ok:
                print(f"\t\033[91m{msg}\033[0m")
                continue

            print("\t\033[93memail and password formats acceptable\033[0m")

            existing = self.controller.find_by_email(email)
            if existing:
                print(f"\t\033[91mStudent {existing.name} already exists\033[0m")
                return
            break

        name = input("\tName: ").strip()
        if not name:
            print("\t\033[91mName cannot be empty.\033[0m")
            return

        ok, msg = self.controller.register(name, email, password)
        color = "\033[93m" if ok else "\033[91m"
        print(f"\t{color}{msg}\033[0m")

    def login(self):
        """Handle student login flow."""
        print("\t\033[92mStudent Sign In\033[0m")

        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()

            success, reason = self.controller.login(email, password)

            if success:
                print("\t\033[93memail and password formats acceptable\033[0m")
                # current_student is set inside controller.login(...)
                self.subject_menu()
                break

            # Handle error messages
            if reason == "bad_format":
                print("\t\033[91mIncorrect email or password format\033[0m")
            elif reason in ("no_such_user", "bad_password"):
                print("\t\033[93memail and password formats acceptable\033[0m")
                print("\t\033[91mStudent does not exist\033[0m")
                break
            else:
                print("\t\033[91mInvalid credentials.\033[0m")

    # ---------- Subject menu & actions ----------

    def subject_menu(self):
        """Display subject menu for enrolled students."""
        while True:
            choice = input("\t\t\033[96mStudent Course Menu (c/e/r/s/x): \033[0m").strip().lower()
            if choice == "c":
                self.change_password()
            elif choice == "e":
                self._enrol_subject_flow()
            elif choice == "r":
                self._remove_subject_flow()
            elif choice == "s":
                self._show_subjects_flow()
            elif choice == "x":
                break
            else:
                continue

    def _enrol_subject_flow(self):
        """Enroll the student in a subject (auto-selected)."""
        ok, msg, sub = self.controller.enrol_auto()
        if ok and sub:
            print(f"\t\t\033[93mEnrolling in {sub.title}\033[0m")
            print(f"\t\t\033[93mYou are now enrolled in {len(self.controller.list_subjects())} out of 4 subjects")
        else:
            print(f"\t\t\033[91m{msg}\033[0m")

    def _show_subjects_flow(self):
        """Display all subjects the student is enrolled in."""
        items = self.controller.list_subjects()
        print(f"\t\t\033[93mShowing {len(items)} subject{'s' if len(items) != 1 else ''}\033[0m")
        for s in items:
            print(f"\t\t[  {s.title}  -- mark = {s.mark} -- grade =  {s.grade}  ]")

    def _remove_subject_flow(self):
        """Remove a subject by ID (matches expected output format)."""
        sid = input("\t\tRemove Subject by ID: ").strip()
        print(f"\t\t\033[93mDroping Subject-{sid}\033[0m")  # Note: "Droping" kept as per sample
        ok, msg = self.controller.remove_by_id(sid)
        print(f"\t\t{'\033[93m' if ok else '\033[91m'}{msg}\033[0m")

    def change_password(self):
        """Handle password update flow."""
        print("\t\t\033[93mUpdating Password\033[0m")

        while True:
            new_pwd = input("\t\tNew Password: ").strip()
            confirm = input("\t\tConfirm Password: ").strip()
            ok, msg = self.controller.change_password(new_pwd, confirm)
            if not ok:
                print(f"\t\t\033[91m{msg}\033[0m")
                continue
            break

    def show_average(self):
        """Display average mark across enrolled subjects."""
        avg = self.controller.average()
        if avg is None:
            print("\t\t\033[93mNo subjects yet; average unavailable.\033[0m")
        else:
            print(f"\t\tAverage mark = {avg:.2f}")

    # ---------- Helpers ----------

    def _validate_formats(self, email: str, password: str) -> tuple[bool, str]:
        """Check email/password format using model validators."""
        from models.user_model import User
        if not User.validate_email(email) or not User.validate_password(password):
            return False, "Incorrect email or password format"
        return True, "OK"
