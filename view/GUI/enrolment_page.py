import tkinter as tk
from tkinter import ttk
from controller.subject_controller import SubjectController
from db.database import Database
from resources.parameters.app_parameters import ENROLLMENT_CONFIG
from view.GUI.base_page import BasePage
from components.label_component import LabelComponent
from components.button_component import ButtonComponent
from components.text_input_component import TextInputComponent
from components.message_box_component import MessageBoxComponent

class EnrolmentPage(BasePage):
    """
    GUI page for student enrolment management.
    Displays student info, enrolment actions, and subject table.
    """

    def __init__(self, master, controller=None, app=None):
        super().__init__(master, bg="white", layout="grid")
        self.controller = controller
        self.db = Database()
        self.subjects = SubjectController(self.db)
        self.app = app

        self.controller.current_student = getattr(controller, "current_student", None)
        self.subjects.set_current_student(self.controller.current_student)

        self._init_vars()
        self._build_layout()

    def _init_vars(self):
        """Initialize UI variables for dynamic labels."""
        self.info_var = tk.StringVar()
        self.avg_var = tk.StringVar(value="Average: 0.00")
        self.status_var = tk.StringVar(value="Status: -")

    def _create_label_frame(self):
        """Create the main container frame with styling from config."""
        self.form_container = tk.LabelFrame(
            self,
            text=ENROLLMENT_CONFIG["subtitle_text"],
            bg=ENROLLMENT_CONFIG["background_color"],
            fg=ENROLLMENT_CONFIG["subtitle_fg"],
            font=ENROLLMENT_CONFIG["subtitle_font"],
            padx=20,
            pady=20
        )
        self.form_container.pack(fill="both", padx=50, pady=50)
        self.form_container.columnconfigure(0, weight=1)
        self.form_container.columnconfigure(1, weight=3)

    def _build_layout(self):
        """Build all layout sections."""
        self._create_label_frame()
        self._build_header()
        self._build_action_buttons()
        self._refresh_status()

    def _build_header(self):
        """Display student info, average, and status."""
        header_frame = tk.Frame(self.form_container, bg="white")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=12, pady=(10, 4))
        header_frame.columnconfigure((0, 1), weight=1)

        LabelComponent(header_frame, textvariable=self.info_var,
                       font=("Segoe UI", 14, "bold"), fg="#333", bg="white", layout="grid").render().grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        LabelComponent(header_frame, textvariable=self.avg_var,
                       font=("Segoe UI", 12), bg="white", layout="grid").render().grid(
            row=1, column=0, sticky="w")

        LabelComponent(header_frame, textvariable=self.status_var,
                       font=("Segoe UI", 12), bg="white", layout="grid").render().grid(
            row=1, column=1, sticky="w")

        student = self.controller.current_student
        if student:
            avg = student.average_mark()
            if avg is None:
                avg = 0.00 

            self.info_var.set(f"HI, {student.name}\nEmail: {student.email}\n")
            self.avg_var.set(f"Average: {avg:.2f}")
            self.status_var.set(f"Status: {'PASS' if student.has_passed() else 'FAIL'}")
        else:
            self.info_var.set("Error: No student loaded.")
            self.avg_var.set("Average: 0.00")
            self.status_var.set("Status: -")

    def _build_action_buttons(self):
        """Create action buttons for enrolment and logout."""
        frame = tk.Frame(self.form_container, bg="white")
        frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=12, pady=8)
        frame.columnconfigure((0, 1, 2), weight=1)

        actions = [
            ("Add Enrollment", self._popup_enrol),
            ("Show Enrollment", self._popup_subject_table),
            ("Logout", self._on_logout)
        ]

        for i, (label, command) in enumerate(actions):
            btn = ButtonComponent(frame, name=label, action=command,
                                  fg="#fff", bg="#007BFF", layout="grid", padding=(6, 6))
            btn.create_component()
            btn.button_widget.grid(row=0, column=i, padx=6, pady=6, sticky="ew")

    def _refresh_status(self):
        """Update average and status labels."""
        student = self.controller.current_student
        if not student:
            self.avg_var.set("Average: 0.00")
            self.status_var.set("Status: -")
            return

        avg = self.controller.current_student.average_mark()
        if avg is None:
            avg = 0.00  

        status = "PASS" if self.controller.current_student.has_passed() else "FAIL"
        self.avg_var.set(f"Average: {avg:.2f}")
        self.status_var.set(f"Status: {status}")


    def _popup_subject_table(self):
        """Show popup window with enrolled subjects in a table."""
        if not self.controller.current_student:
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

        tree = self._create_treeview(frame)
        self._populate_subjects(tree)

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

        self._refresh_status()

    def _create_treeview(self, parent):
        """Create Treeview widget for subject display."""
        tree = ttk.Treeview(parent, columns=("id", "title", "mark", "grade"), show="headings", height=8)
        for col, label in [("id", "ID"), ("title", "Title"), ("mark", "Mark"), ("grade", "Grade")]:
            tree.heading(col, text=label)
            tree.column(col, anchor="center" if col != "title" else "w", width=80 if col != "title" else 260)
        tree.grid(row=0, column=0, sticky="nsew")
        return tree

    def _populate_subjects(self, tree):
        """Insert subject data into Treeview."""
        for subj in self.controller.current_student.subjects:
            tree.insert("", "end", values=(subj.id, subj.title, subj.mark, subj.grade))

    def _popup_enrol(self):
        """Trigger auto-enrolment and show result."""
        if not self.controller.current_student:
            self._show_message("Error", "No student loaded.")
            return

        ok, msg, _ = self.subjects.enrol_auto()
        self._refresh_status()
        self._show_message("Success" if ok else "Error", msg)

    def _on_logout(self):
        """Handle logout and navigate to login page."""
        print("[DEBUG][Enrollment Page] -> login")
        if self.app:
            self.app.navigate("login")

    def _show_message(self, title, message):
        """Display a modal message box."""
        MessageBoxComponent(
            self.master,
            title=title,
            message=message,
            width=400,
            height=200,
            modal=True
        ).show()

