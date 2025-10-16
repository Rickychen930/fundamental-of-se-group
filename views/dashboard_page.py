from views.base_page import BasePage
from components.label_component import LabelComponent
from components.button_component import ButtonComponent
from components.form_field_component import FormField  # used in remove/change password
from components.message_box_component import MessageBoxComponent
from view_models.enrolment_view_model import EnrolmentViewModel
from resources.parameters.app_parameters import PAGE_CONFIG, SUBJECT_CATALOG
import tkinter as tk


class DashboardPage(BasePage):
    def __init__(self, master, controller=None):
        super().__init__(master, bg=PAGE_CONFIG["default_bg"])
        self.controller = controller
        self.vm = EnrolmentViewModel()  # enrolment logic

        # attach current user from MainPage session
        if self.controller and hasattr(self.controller, "get_user"):
            user = self.controller.get_user()
            if user:
                self.vm.set_user(user)
            else:
                MessageBoxComponent(self.master, title="Session", message="No logged-in user. Returning to login.", modal=True).show()
                if hasattr(self.controller, "navigate"):
                    self.controller.navigate("login")
                return

        self._build_menu()  # main menu

    # remove all widgets on this page
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    # simple popup helper
    def _msg(self, title: str, message: str):
        MessageBoxComponent(self.master, title=title, message=message, modal=True).show()

    # main menu
    def _build_menu(self):
        self._clear()
        self.set_title("Enrolment")
        LabelComponent(self, text="Choose an action:", font=("Segoe UI", 12)).render()

        # summary ID - Title
        subs = self.vm.list_subjects()
        LabelComponent(self, text=f"Enrolled: {len(subs)}/4").render()
        for s in subs:
            LabelComponent(self, text=f"{s['id']} - {s['title']}").render()

        b1 = ButtonComponent(self, name="(e) Enrol in a subject", action=self._build_enrol)
        b1.create_component(); b1.render()

        b2 = ButtonComponent(self, name="(s) Show enrolled subjects", action=self._show_subjects)
        b2.create_component(); b2.render()

        b3 = ButtonComponent(self, name="(r) Remove a subject", action=self._build_remove)
        b3.create_component(); b3.render()

        b4 = ButtonComponent(self, name="(c) Change password", action=self._build_change_password)
        b4.create_component(); b4.render()

        b5 = ButtonComponent(self, name="(x) Exit (logout)", action=self._logout)
        b5.create_component(); b5.render()

    #   enrol UI with a combobox of subject names
    def _build_enrol(self):
        self._clear()
        LabelComponent(self, text="Enrol in a Subject (max 4)", font=("Segoe UI", 12)).render()

        LabelComponent(self, text="Subject").render()
        self.subject_var = tk.StringVar()
        self.subject_combo = self.ttk.Combobox(
            self,
            textvariable=self.subject_var,
            values=SUBJECT_CATALOG,
            state="readonly",
            width=35
        )
        if SUBJECT_CATALOG:
            self.subject_combo.current(0)
        self.subject_combo.pack(padx=10, pady=10)

        enrol_btn = ButtonComponent(self, name="Enrol", action=self._enrol)
        enrol_btn.create_component(); enrol_btn.render()

        back_btn = ButtonComponent(self, name="Back", action=self._build_menu)
        back_btn.create_component(); back_btn.render()

    #  enrol perform enrolment (ID 001..999 )
    def _enrol(self):
        title = (self.subject_combo.get() or "").strip() if hasattr(self, "subject_combo") else ""
        if not title:
            self._msg("Enrolment", "Please choose a subject.")
            return

        ok, data = self.vm.enrol(subject_title=title)  # VM creates 3-digit ID
        if not ok:
            self._msg("Enrolment", data.get("message", "Cannot enrol."))
            return

        self._msg("Enrolment", f"Enrolled in {data['title']} (ID {data['id']}).")
        self._show_subjects()  # auto-show list after enrol

    #  show list enrolled subjects (ID + Title)
    def _show_subjects(self):
        self._clear()
        LabelComponent(self, text="Enrolled Subjects", font=("Segoe UI", 12)).render()

        subjects = self.vm.list_subjects()
        if not subjects:
            LabelComponent(self, text="No subjects enrolled.").render()
        else:
            for s in subjects:
                LabelComponent(self, text=f"{s['id']} - {s['title']}").render()

        go_remove = ButtonComponent(self, name="Go to remove", action=self._build_remove)
        go_remove.create_component(); go_remove.render()

        back_btn = ButtonComponent(self, name="Back", action=self._build_menu)
        back_btn.create_component(); back_btn.render()

    #  remove UI to remove by ID
    def _build_remove(self):
        self._clear()
        LabelComponent(self, text="Remove a Subject", font=("Segoe UI", 12)).render()

        self.remove_field = FormField(self, label_text="Subject ID")  # expects 3-digit id
        self.remove_field.render()

        rm_btn = ButtonComponent(self, name="Remove", action=self._remove)
        rm_btn.create_component(); rm_btn.render()

        back_btn = ButtonComponent(self, name="Back", action=self._build_menu)
        back_btn.create_component(); back_btn.render()

    #  remove perform remove by 3-digit ID
    def _remove(self):
        sid = self.remove_field.get_value().strip() if hasattr(self, "remove_field") else ""

        # validate 3-digit ID: 001..999
        if not (sid.isdigit() and len(sid) == 3 and 1 <= int(sid) <= 999):
            self._msg("Remove Subject", "Please enter a valid 3-digit Subject ID (001..999).")
            return

        ok, msg = self.vm.remove(sid)
        self._msg("Remove Subject", msg)
        self._show_subjects()

    #  change: UI for password change
    def _build_change_password(self):
        self._clear()
        LabelComponent(self, text="Change Password", font=("Segoe UI", 12)).render()

        self.pwd_field = FormField(self, label_text="New password")
        self.pwd_field.render()

        upd_btn = ButtonComponent(self, name="Update Password", action=self._change_password)
        upd_btn.create_component(); upd_btn.render()

        back_btn = ButtonComponent(self, name="Back", action=self._build_menu)
        back_btn.create_component(); back_btn.render()

    #  change: perform password update
    def _change_password(self):
        new_pwd = self.pwd_field.get_value().strip() if hasattr(self, "pwd_field") else ""
        ok, msg = self.vm.change_password(new_pwd)
        self._msg("Change Password", msg)
        if ok:
            self._build_menu()

    #  exit: back to login page
    def _logout(self):
        if self.controller and hasattr(self.controller, "navigate"):
            self.controller.navigate("login")
