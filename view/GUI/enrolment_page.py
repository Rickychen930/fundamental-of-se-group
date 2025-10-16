import tkinter as tk
from tkinter import ttk
from view.GUI.base_page import BasePage
from components.label_component import LabelComponent
from components.button_component import ButtonComponent
from components.text_input_component import TextInputComponent
from components.message_box_component import MessageBoxComponent
from components.form_row_component import FormRowComponent  # Make sure this exists

class EnrolmentPage(BasePage):
    def __init__(self, master, controller=None, app=None):
        super().__init__(master, bg="white", layout="grid")
        self.controller = controller
        self.app = app
        self.student = getattr(controller, "current_student", None)

        self._init_vars()
        self._build_header()
        self._build_subject_table()
        self._build_enrol_section()
        self._build_remove_section()
        self._build_password_section()
        self._build_footer()
        self._refresh_view()

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

    def _build_subject_table(self):
        frame = tk.LabelFrame(self, text="Enrolled Subjects", bg="white")
        frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=12, pady=8)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(frame, columns=("id", "title", "mark", "grade"), show="headings", height=8)
        for col, label in [("id", "ID"), ("title", "Title"), ("mark", "Mark"), ("grade", "Grade")]:
            self.tree.heading(col, text=label)
            self.tree.column(col, anchor="center" if col != "title" else "w", width=80 if col != "title" else 260)
        self.tree.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

    def _build_enrol_section(self):
        frame = tk.LabelFrame(self, text="Enrol in a Subject", bg="white")
        frame.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        frame.columnconfigure(1, weight=1)

        self.enrol_row = FormRowComponent(
            frame,
            label_text="Subject title:",
            button_text="Enrol",
            button_action=self._on_enrol
        )
        self.enrol_row.get_widget().grid(row=0, column=0, columnspan=3, sticky="ew")

    def _build_remove_section(self):
        frame = tk.LabelFrame(self, text="Remove a Subject", bg="white")
        frame.grid(row=3, column=1, sticky="ew", padx=12, pady=8)
        frame.columnconfigure(1, weight=1)

        self.remove_row = FormRowComponent(
            frame,
            label_text="Subject ID:",
            button_text="Remove",
            button_action=self._on_remove
        )
        self.remove_row.get_widget().grid(row=0, column=0, columnspan=3, sticky="ew")

    def _build_password_section(self):
        frame = tk.LabelFrame(self, text="Change Password", bg="white")
        frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=12, pady=8)
        frame.columnconfigure(1, weight=1)

        self.password_row = FormRowComponent(
            frame,
            label_text="New password:",
            button_text="Update Password",
            button_action=self._on_change_password,
            show="*"
        )
        self.password_row.get_widget().grid(row=0, column=0, columnspan=3, sticky="ew")

    def _build_footer(self):
        frame = tk.Frame(self, bg="white")
        frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=12, pady=12)
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

    def _refresh_view(self):
        self.tree.delete(*self.tree.get_children())
        if not self.student:
            return
        for subj in self.student.subjects:
            self.tree.insert("", "end", values=(subj.id, subj.title, subj.mark, subj.grade))
        avg = self.student.average_mark()
        self.avg_var.set(f"Average: {avg:.2f}")
        self.status_var.set(f"Status: {'PASS' if self.student.has_passed() else 'FAIL'}")

    # ------------------ Actions ------------------
    def _on_enrol(self):
        title = self.enrol_row.get_input().get_text()
        if not title:
            self._show_message("Error", "Subject title cannot be empty.")
            return
        success, msg = self.controller.enrol_subject(title)
        if success:
            self.enrol_row.get_input().set_text("")
            self._refresh_view()
        else:
            self._show_message("Enrol Error", msg)

    def _on_remove(self):
        sid = self.remove_row.get_input().get_text()
        if not sid:
            self._show_message("Error", "Enter a Subject ID to remove.")
            return
        success, msg = self.controller.remove_subject(sid)
        if success:
            self.remove_row.get_input().set_text("")
            self._refresh_view()
        else:
            self._show_message("Remove Error", msg)

    def _on_change_password(self):
        new_pw = self.password_row.get_input().get_text()
        if not new_pw:
            self._show_message("Error", "Enter a new password.")
            return
        success, msg = self.controller.change_password(new_pw)
        if success:
            self.password_row.get_input().set_text("")
            self._show_message("Success", msg)
        else:
            self._show_message("Password Error", msg)

    def _on_logout(self):
        self.controller.logout()
        self.controller.navigate("login")

    def _show_message(self, title, message):
        popup = MessageBoxComponent(self.master, title=title, message=message, width=400, height=200, modal=True)
        popup.show()
