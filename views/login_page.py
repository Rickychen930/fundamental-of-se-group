from tkinter import Frame, Label
from components.form_field_component import FormField
from components.button_component import ButtonComponent
from views.base_page import BasePage
from view_models.login_view_model import LoginViewModel
from resources.parameters.app_parameters import LOGIN_CONFIG

class LoginPage(BasePage):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        self.view_model = LoginViewModel()
        self.cfg = LOGIN_CONFIG

        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        self.set_background_color(self.cfg.get("background_color"))
        self.set_title(
            self.cfg.get("title_text", "Login"),
            font=self.cfg.get("title_font"),
            pady=self.cfg.get("title_padding")
        )

        self.center_frame = self.add_centered_frame()
        self._create_subtitle()
        self._create_form_fields()
        self._create_message_label()
        self._create_buttons()

    def _create_subtitle(self):
        self.subtitle = Label(
            self.center_frame,
            text=self.cfg.get("subtitle_text", "Please log in to continue"),
            font=self.cfg.get("subtitle_font"),
            bg=self["bg"],
            fg=self.cfg.get("subtitle_fg")
        )
        self.subtitle.pack(pady=(0, 10))

    def _create_form_fields(self):
        self.form_frame = Frame(self.center_frame, bg=self["bg"])
        self.form_frame.pack(
            pady=self.cfg.get("form_padding_y"),
            padx=self.cfg.get("form_padding_x"),
            fill="x"
        )

        # Create fields
        self.username_field = FormField(self.form_frame, **self._field_config("username"))
        self.password_field = FormField(self.form_frame, **self._field_config("password"))

        # Create components (but don't pack)
        self.username_field.create_component()
        self.password_field.create_component()

        # Use grid layout
        self.username_field.label_widget.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
        self.username_field.input_widget.grid(row=0, column=1, sticky="w", pady=5)

        self.password_field.label_widget.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        self.password_field.input_widget.grid(row=1, column=1, sticky="w", pady=5)

    def _field_config(self, field_type):
        return {
            "label_text": self.cfg.get(f"{field_type}_label", field_type.capitalize()),
            "label_style": self.cfg.get("field_label_style"),
            "label_font": self.cfg.get("field_label_font"),
            "input_width": self.cfg.get("input_width"),
            "input_font": self.cfg.get("input_font"),
            "input_fg": self.cfg.get("input_fg"),
            "input_bg": self.cfg.get("input_bg"),
            "padding": self.cfg.get("input_padding"),
            "autoselect": field_type == "username"
        }

    def _create_message_label(self):
        self.message_label = Label(
            self.center_frame,
            text="",
            font=("Segoe UI", 10),
            bg=self["bg"],
            fg=self.cfg.get("subtitle_fg", "#555")
        )
        self.message_label.pack(pady=(6, 0))

    def _create_buttons(self):
        self.button_frame = Frame(self.center_frame, bg=self["bg"])
        self.button_frame.pack(pady=self.cfg.get("button_frame_padding"))

        self.login_button = ButtonComponent(
            self.button_frame,
            name=self.cfg.get("button_text", "Login"),
            action=self.handle_login,
            style=self.cfg.get("button_style"),
            layout=self.cfg.get("button_layout"),
            padding=self.cfg.get("button_padding")
        )

        self.register_button = None
        if self.cfg.get("register_button_text"):
            self.register_button = ButtonComponent(
                self.button_frame,
                name=self.cfg.get("register_button_text", "Register"),
                action=self.handle_register,
                style=self.cfg.get("register_button_style"),
                layout=self.cfg.get("register_button_layout"),
                padding=self.cfg.get("register_button_padding")
            )

        self.login_button.create_component()
        self.login_button.render()
        if self.register_button:
            self.register_button.create_component()
            self.register_button.render()

    def _bind_events(self):
        self.bind_all("<Return>", lambda e: self.handle_login())

    def set_message(self, text, kind="info"):
        color_map = {
            "error": "#C62828",
            "ok": "#2E7D32",
            "info": self.cfg.get("subtitle_fg", "#555")
        }
        self.message_label.config(text=text, fg=color_map.get(kind, "#555"))

    def handle_login(self):
        self._set_login_button_state("disabled")

        username = self.username_field.get_value()
        password = self.password_field.get_value()

        if not username or not password:
            self.set_message("Username and password cannot be empty.", kind="error")
            self._set_login_button_state("normal")
            return

        self.view_model.set_credentials(username, password)
        is_valid, message = self.view_model.validate_credentials()

        if not is_valid:
            self.set_message(message, kind="error")
            self._set_login_button_state("normal")
            return

        try:
            success, login_message = self.view_model.login()
            if success:
                self.set_message(login_message, kind="ok")
                if self.controller and hasattr(self.controller, "navigate"):
                    self.controller.navigate("home")
                else:
                    print("✅ Navigating to home page...")
            else:
                self.set_message(login_message or "Login failed.", kind="error")
        except Exception as e:
            self.set_message(f"An error occurred: {e}", kind="error")
        finally:
            self._set_login_button_state("normal")

    def _set_login_button_state(self, state):
        if hasattr(self.login_button, "set_state"):
            try:
                self.login_button.set_state(state)
            except Exception:
                pass

    def handle_register(self):
        if self.controller and hasattr(self.controller, "navigate"):
            self.controller.navigate("register")
        else:
            self.set_message("Register feature is not available yet.", kind="info")
