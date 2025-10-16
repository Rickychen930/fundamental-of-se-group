from view.CLI.base_page import BasePage
from controller.subject_controller import SubjectController
from db.database import Database


class StudentPage(BasePage):
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

        # 1) Loop until email/password format is acceptable
        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()

            valid, msg = self.controller.validate_credentials(email, password)
            if not valid:
                # e.g. "Incorrect email or password format"
                print(f"\t\033[91m{msg}\033[0m")
                continue

            # e.g. "email and password formats acceptable"
            print(f"\t\033[93m{msg}\033[0m")
            break

        # 2) Ask for name (simple non-empty check optional)
        name = input("\tName: ").strip()
        if not name:
            print("\t\033[91mName cannot be empty.\033[0m")
            return

        # 3) Call controller.register and print based on success/failure
        try:
            ok, msg = self.controller.register(name, email, password)
            # Expected:
            #  - ok=True,  msg="Enrolling Student John Smith"
            #  - ok=False, msg="Student John Smith already exists"
            color = "\033[92m" if ok else "\033[91m"
            print(f"\t{color}{msg}\033[0m")
        except Exception as ex:
            # In case Student.create raises validation errors, etc.
            print(f"\t\033[91mRegistration failed: {ex}\033[0m")



    def login(self):
        print("\t\033[92mStudent Sign In\033[0m")
        email = input("\tEmail: ").strip()
        password = input("\tPassword: ").strip()

        success, reason = self.controller.login(email, password)

        if success:
            # Match the sample transcript: show this line before the course menu
            print("\t\033[93memail and password formats acceptable\033[0m")
            self.subjects.set_current_student(self.controller.current_student)
            self.subject_menu()
            return

        # Failure cases
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


    def subject_menu(self):
        student = self.controller.current_student
        while True:
            # ✅ No end=... here; that's only for print()
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
        ok, msg, sub = self.subjects.enrol_auto()
        if ok:
            print(f"\t\033[93m{msg}\033[0m")
        else:
            print(f"\t\033[91m{msg}\033[0m")

    def _show_subjects_flow(self, student):
        items = self.subjects.list_subjects()
        print(f"\tShowing {len(items)} subject{'s' if len(items)!=1 else ''}")
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
        print(f"\tDroping {sid}")
        ok, msg = self.subjects.remove_by_id(sid)
        if ok:
            print(f"\t\033[93m{msg}\033[0m")
        else:
            print(f"\t\033[91m{msg}\033[0m")

    def change_password(self, student):
        print("\t\033[96mUpdating password")
        new_pwd = input("\tNew Password: ").strip()
        confirm = input("\tConfirm Password: ").strip()
        ok, msg = self.subjects.change_password(new_pwd, confirm)
        if ok:
            print(f"\t\033[93m{msg}\033[0m")
        else:
            print(f"\t\033[91m{msg}\033[0m")

    def show_average(self, student):
        avg = self.subjects.average()
        if avg is None:
            print("\t\033[93mNo subjects yet; average unavailable.\033[0m")
        else:
            print(f"\tAverage mark = {avg:.2f}")
