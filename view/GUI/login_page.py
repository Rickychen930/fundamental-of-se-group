import tkinter as tk
from components.form_field_component import FormField
from components.button_component import ButtonComponent
from components.label_component import LabelComponent
from components.message_box_component import MessageBoxComponent
from resources.parameters.app_parameters import LOGIN_CONFIG
from view.GUI.base_page import BasePage

class LoginPage(BasePage):
    """
    LoginPage handles user authentication UI.
    It includes form fields for email and password, and routes users based on role.
    """

    def __init__(self, master, controller=None, db=None, app=None):
        super().__init__(master, bg=LOGIN_CONFIG["background_color"])
        self.controller = controller
        self.db = db
        self.app = app

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._create_label_frame()
        self._create_form_fields()
        self._create_buttons()

    def _create_label_frame(self):
        """Create the labeled frame container for the login form."""
        self.form_container = tk.LabelFrame(
            self,
            text=LOGIN_CONFIG["subtitle_text"],
            bg=LOGIN_CONFIG["background_color"],
            fg=LOGIN_CONFIG["subtitle_fg"],
            font=LOGIN_CONFIG["subtitle_font"],
            padx=20,
            pady=20
        )
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")
        self.form_container.columnconfigure(0, weight=1)
        self.form_container.columnconfigure(1, weight=3)

    def _create_form_fields(self):
        """Create and place the email and password fields."""
        # Email field
        email_cfg = self._field_config("username")
        email_cfg["label_text"] = "Email"
        self.username_field = FormField(self.form_container, textvariable=self.username_var, **email_cfg)

        # Password field
        pwd_cfg = self._field_config("password")
        pwd_cfg["show"] = "*"
        self.password_field = FormField(self.form_container, textvariable=self.password_var, **pwd_cfg)

        # Render fields
        self.username_field.create_component()
        self.password_field.create_component()

        # Grid placement
        self.username_field.label_widget.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_field.input_widget.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.username_field.input_widget.focus()

        self.password_field.label_widget.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_field.input_widget.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Keyboard navigation
        self.username_field.input_widget.bind("<Return>", lambda e: self.password_field.input_widget.focus_set())
        self.password_field.input_widget.bind("<Return>", lambda e: self._handle_login())

    def _create_buttons(self):
        """Create and place the login and cancel buttons."""
        self.cancel_button = ButtonComponent(
            self.form_container,
            name=LOGIN_CONFIG["cancel_text"],
            action=self.master.quit,
            style=LOGIN_CONFIG["register_button_style"],
            layout=LOGIN_CONFIG["button_layout"],
            padding=(5, 5)
        )
        self.login_button = ButtonComponent(
            self.form_container,
            name=LOGIN_CONFIG["button_text"],
            action=self._handle_login,
            style=LOGIN_CONFIG["button_style"],
            layout=LOGIN_CONFIG["button_layout"],
            padding=(5, 5)
        )

        self.cancel_button.create_component()
        self.login_button.create_component()

        # Place both buttons in the same row, aligned left and right
        self.cancel_button.button_widget.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.login_button.button_widget.grid(row=3, column=1, sticky="e", padx=5, pady=5)

    def _field_config(self, field_type):
        """Return configuration dictionary for a given field type."""
        return {
            "label_text": LOGIN_CONFIG[f"{field_type}_label"],
            "label_style": LOGIN_CONFIG["field_label_style"],
            "label_font": LOGIN_CONFIG["field_label_font"],
            "label_fg": LOGIN_CONFIG["subtitle_fg"],
            "label_bg": LOGIN_CONFIG["background_color"],
            "input_width": LOGIN_CONFIG["input_width"],
            "input_font": LOGIN_CONFIG["input_font"],
            "input_fg": LOGIN_CONFIG["input_fg"],
            "input_bg": LOGIN_CONFIG["input_bg"],
            "padding": LOGIN_CONFIG["input_padding"],
            "autoselect": field_type == "username"
        }

    def _handle_login(self):
        """Validate credentials and route user based on role."""
        email = self.username_field.get_value()
        password = self.password_field.get_value()
        print(f"[DEBUG][LoginPage] Login attempt email={email}")

        try:
            success, result = self.controller.login(email, password)
            print(f"[DEBUG][LoginPage] Login result: {success}, {result}")

            if success:
                student = self.controller.current_student
                role = getattr(student, "role", "student").lower()
                target_page = "admin" if role == "admin" else "enrolment"
                print(f"[DEBUG][LoginPage] Routing by role={role} -> {target_page}")
                self._clear_fields()
                if self.app:
                    self.app.navigate(target_page)
            else:
                message = result.get("message") if isinstance(result, dict) else "Invalid credentials."
                self._show_message("Login Error", message)
                self._clear_fields()

        except Exception as e:
            print(f"[ERROR][LoginPage] Exception: {e}")
            self._show_message("Login Error", f"An error occurred: {e}")
            self._clear_fields()

    def _show_message(self, title, message):
        """Display a modal message box with the given title and message."""
        popup = MessageBoxComponent(
            self.master,
            title=title,
            message=message,
            width=400,
            height=200,
            modal=True
        )
        popup.show()

    def _clear_fields(self):
        """Clear input fields and return focus to the email field."""
        self.username_var.set("")
        self.password_var.set("")
        try:
            self.username_field.input_widget.focus_set()
        except Exception:
            pass
