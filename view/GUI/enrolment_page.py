import tkinter as tk
from tkinter import ttk
from view.GUI.base_page import BasePage
from components.label_component import LabelComponent
from components.button_component import ButtonComponent
from components.text_input_component import TextInputComponent
from components.message_box_component import MessageBoxComponent

class EnrolmentPage(BasePage):
    def __init__(self, master, controller=None, app=None):
        super().__init__(master, bg="white", layout="grid")
        self.controller = controller
        self.app = app
        self.student = getattr(controller, "current_student", None)

        self._init_vars()
        self._build_header()
        self._build_action_buttons()
        self._build_footer()
        self._refresh_status()

    def _init_vars(self):
        self.info_var = tk.StringVar()
        self.avg_var = tk.StringVar(value="Average: 0.00")
        self.status_var = tk.StringVar(value="Status: -")

    def _build_header(self):
        LabelComponent(
            self,
            text="Enrolment",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            layout="grid",
            padding=(16, 8)
        ).render()

        LabelComponent(
            self,
            textvariable=self.info_var,
            fg="#333",
            bg="white",
            layout="grid",
            padding=(0, 10)
        ).render()

        if self.student:
            self.info_var.set(f"Logged in as: {self.student.name} ({self.student.email})")
        else:
            self.info_var.set("Error: No student loaded.")

    def _build_action_buttons(self):
        frame = tk.Frame(self, bg="white")
        frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=8)
        frame.columnconfigure((0, 1, 2), weight=1)

        actions = [
            ("Add Enrollment", self._popup_enrol),
            ("Show Enrollment", self._popup_subject_table),
            ("Change Password", self._popup_password)
        ]

        for i, (label, command) in enumerate(actions):
            btn = ButtonComponent(frame, name=label, action=command, layout="grid", padding=(6, 6))
            btn.create_component()
            btn.button_widget.grid(row=0, column=i, padx=6, pady=6, sticky="ew")

    def _build_footer(self):
        frame = tk.Frame(self, bg="white")
        frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=12, pady=12)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        LabelComponent(
            frame,
            textvariable=self.avg_var,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            layout="grid",
            padding=(0, 0)
        ).render()
        LabelComponent(
            frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            layout="grid",
            padding=(0, 0)
        ).render()

        btn = ButtonComponent(frame, name="Logout", action=self._on_logout, layout="grid", padding=(6, 6))
        btn.create_component()
        btn.button_widget.grid(row=0, column=2, sticky="e")

    def _refresh_status(self):
        if not self.student:
            self.avg_var.set("Average: 0.00")
            self.status_var.set("Status: -")
            return

        avg = self.student.average_mark()
        status = "PASS" if self.student.has_passed() else "FAIL"
        self.avg_var.set(f"Average: {avg:.2f}")
        self.status_var.set(f"Status: {status}")

    def _popup_subject_table(self):
        if not self.student:
            self._show_message("Error", "No student data available.")
            return

        popup = tk.Toplevel(self)
        popup.title("Enrolled Subjects")
        popup.geometry("600x300")
        popup.transient(self)
        popup.grab_set()

        frame = tk.LabelFrame(popup, text="Subjects", bg="white")
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        tree = ttk.Treeview(frame, columns=("id", "title", "mark", "grade"), show="headings", height=8)
        for col, label in [("id", "ID"), ("title", "Title"), ("mark", "Mark"), ("grade", "Grade")]:
            tree.heading(col, text=label)
            tree.column(col, anchor="center" if col != "title" else "w", width=80 if col != "title" else 260)
        tree.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

        for subj in self.student.subjects:
            tree.insert("", "end", values=(subj.id, subj.title, subj.mark, subj.grade))

        self._refresh_status()

    def _popup_enrol(self):
        popup = tk.Toplevel(self)
        popup.title("Add Enrollment")
        popup.geometry("320x160")
        popup.transient(self)
        popup.grab_set()

        form_frame = tk.Frame(popup, bg="white")
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)

        LabelComponent(form_frame, text="Subject Title:", bg="white").render()
        input_field = TextInputComponent(form_frame)
        input_field.render()
        input_field.get_widget().pack(fill="x", pady=6)

        def submit():
            title = input_field.get_text()
            if not title:
                self._show_message("Error", "Subject title cannot be empty.")
            else:
                success, msg = self.controller.enrol_subject(title)
                if success:
                    self._refresh_status()
                    popup.destroy()
                else:
                    self._show_message("Enrol Error", msg)

        btn = ButtonComponent(form_frame, name="Submit", action=submit)
        btn.create_component()
        btn.button_widget.pack(pady=10)

    def _popup_password(self):
        popup = tk.Toplevel(self)
        popup.title("Change Password")
        popup.geometry("320x220")
        popup.transient(self)
        popup.grab_set()

        form_frame = tk.Frame(popup, bg="white")
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)

        LabelComponent(form_frame, text="New Password:", bg="white").render()
        input_pw1 = TextInputComponent(form_frame, show="*")
        input_pw1.render()
        input_pw1.get_widget().pack(fill="x", pady=6)

        LabelComponent(form_frame, text="Confirm Password:", bg="white").render()
        input_pw2 = TextInputComponent(form_frame, show="*")
        input_pw2.render()
        input_pw2.get_widget().pack(fill="x", pady=6)

        def submit():
            pw1 = input_pw1.get_text()
            pw2 = input_pw2.get_text()

            if not pw1 or not pw2:
                self._show_message("Error", "Both password fields must be filled.")
                popup.destroy()
                return

            if pw1 != pw2:
                self._show_message("Error", "Passwords do not match.")
                popup.destroy()
                return

            success, msg = self.controller.change_password(pw1)
            if success:
                self._show_message("Success", msg)
            else:
                self._show_message("Password Error", msg)
            popup.destroy()

        btn = ButtonComponent(form_frame, name="Update", action=submit)
        btn.create_component()
        btn.button_widget.pack(pady=10)

    def _on_logout(self):
        target_page = "login"
        print(f"[DEBUG][Enrollment Page] -> {target_page}")
        if self.app:
            self.app.navigate(target_page)

    def _show_message(self, title, message):
        popup = MessageBoxComponent(self.master, title=title, message=message, width=400, height=200, modal=True)
        popup.show()
