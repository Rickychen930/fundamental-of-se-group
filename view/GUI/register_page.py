from tkinter import Frame, Label
from components.form_field_component import FormField
from components.button_component import ButtonComponent
from view.GUI.base_page import BasePage
from resources.parameters.app_parameters import REGISTER_CONFIG

class RegisterPage(BasePage):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        self.cfg = REGISTER_CONFIG

        self._setup_ui()
        self._create_components()
        self._render_form_fields()
        self._render_buttons()

    def _setup_ui(self):
        self.set_background_color(self.cfg["background_color"])
        self.set_title(
            self.cfg["title_text"],
            font=self.cfg["title_font"],
            pady=self.cfg["title_padding"]
        )

        self.center_frame = self.add_centered_frame()

        self.subtitle = Label(
            self.center_frame,
            text=self.cfg.get("subtitle_text", "Create a new account to start using the app"),
            font=self.cfg.get("subtitle_font", ("Arial", 12)),
            bg=self["bg"],
            fg=self.cfg.get("subtitle_fg", "#555")
        )
        self.subtitle.pack(pady=(0, 10))

        self.form_frame = Frame(self.center_frame, bg=self["bg"])
        self.form_frame.pack(pady=10, padx=20, fill="x")

        self.username_field = FormField(self.form_frame, **self._field_config("username"))
        self.email_field = FormField(self.form_frame, **self._field_config("email"))
        self.password_field = FormField(self.form_frame, **self._field_config("password"))

        self.button_frame = Frame(self.center_frame, bg=self["bg"])
        self.button_frame.pack(pady=20)

        self.register_button = ButtonComponent(
            self.button_frame,
            name=self.cfg["button_text"],
            action=self.handle_register,
            style=self.cfg["button_style"],
            layout=self.cfg["button_layout"],
            padding=self.cfg["button_padding"]
        )

        self.back_button = ButtonComponent(
            self.button_frame,
            name=self.cfg.get("back_button_text", "Back"),
            action=self.handle_back,
            style=self.cfg.get("back_button_style", "Secondary.TButton"),
            layout=self.cfg.get("back_button_layout", "pack"),
            padding=self.cfg.get("back_button_padding", (20, 10))
        )

    def _field_config(self, field_type):
        return {
            "label_text": self.cfg[f"{field_type}_label"],
            "label_style": self.cfg["field_label_style"],
            "label_font": self.cfg["field_label_font"],
            "input_width": self.cfg["input_width"],
            "input_font": self.cfg["input_font"],
            "input_fg": self.cfg["input_fg"],
            "input_bg": self.cfg["input_bg"],
            "padding": self.cfg["input_padding"],
            "autoselect": field_type == "username"
        }

    def _create_components(self):
        self.username_field.create_component()
        self.email_field.create_component()
        self.password_field.create_component()
        self.register_button.create_component()
        self.back_button.create_component()

    def _render_form_fields(self):
        self.username_field.label_widget.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
        self.username_field.input_widget.grid(row=0, column=1, sticky="w", pady=5)

        self.email_field.label_widget.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        self.email_field.input_widget.grid(row=1, column=1, sticky="w", pady=5)

        self.password_field.label_widget.grid(row=2, column=0, sticky="e", padx=(0, 10), pady=5)
        self.password_field.input_widget.grid(row=2, column=1, sticky="w", pady=5)

    def _render_buttons(self):
        self.register_button.render()
        self.back_button.render()

    def handle_register(self):
        name = self.username_field.get_value()
        email = self.email_field.get_value()
        password = self.password_field.get_value()

        success, message = self.controller.register(name, email, password)
        print(message)
        if success:
            print("Registration successful. Navigating to login page...")
            if self.controller and hasattr(self.controller, "navigate"):
                self.controller.navigate("login")

    def handle_back(self):
        if self.controller and hasattr(self.controller, "navigate"):
            self.controller.navigate("login")
        else:
            print("Back navigation not available.")
