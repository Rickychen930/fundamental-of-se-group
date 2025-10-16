import tkinter as tk
from components.form_field_component import FormField
from components.button_component import ButtonComponent
from components.message_box_component import MessageBoxComponent
from view_models.login_view_model import LoginViewModel
from resources.parameters.app_parameters import LOGIN_CONFIG
from views.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, master, controller=None):
        super().__init__(master, bg=LOGIN_CONFIG["background_color"])
        self.controller = controller
        self.view_model = LoginViewModel()

        self._create_title()
        self._create_label_frame()
        self._create_form_fields()
        self._create_buttons()

    def _create_title(self):
        self.title_label = tk.Label(
            self,
            text=LOGIN_CONFIG["title_text"],
            font=LOGIN_CONFIG["title_font"],
            fg=LOGIN_CONFIG["title_fg"],
            bg=LOGIN_CONFIG["background_color"]
        )
        self.title_label.pack(pady=LOGIN_CONFIG["title_padding"])

    def _create_label_frame(self):
        self.form_container = tk.LabelFrame(
            self,
            text=LOGIN_CONFIG["subtitle_text"],
            bg=LOGIN_CONFIG["background_color"],
            fg=LOGIN_CONFIG["subtitle_fg"],
            font=LOGIN_CONFIG["subtitle_font"],
            padx=20,
            pady=20
        )
        self.form_container.pack(pady=10)
        self.form_container.columnconfigure(0, weight=1)
        self.form_container.columnconfigure(1, weight=3)

    def _create_form_fields(self):
        self.username_field = FormField(self.form_container, **self._field_config("username"))
        self.password_field = FormField(self.form_container, **self._field_config("password"))

        self.username_field.create_component()
        self.password_field.create_component()

        self.username_field.label_widget.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_field.input_widget.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.username_field.input_widget.focus()

        self.password_field.label_widget.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_field.input_widget.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    def _create_buttons(self):
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

        self.cancel_button.button_widget.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.login_button.button_widget.grid(row=3, column=1, sticky="e", padx=5, pady=5)

    def _field_config(self, field_type):
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
        username = self.username_field.get_value()
        password = self.password_field.get_value()

        self.view_model.set_credentials(username, password)
        is_valid, message = self.view_model.validate_credentials()

        if not is_valid:
            self._show_message("Login Error", message)
            self._clear_fields()
            return

        try:
            success, login_message = self.view_model.login()
            if success:
                self.controller.set_user(self.view_model.user)
                
                if self.controller and hasattr(self.controller, "navigate"):
                    # self.controller.navigate("home")
                    self.controller.navigate("dashboard")
                    self._clear_fields()

            else:
                self._show_message("Login Error", login_message)
                self._clear_fields()
        except Exception as e:
            self._show_message("Login Error", f"An error occurred: {e}")
            self._clear_fields()

    def _show_message(self, title, message):
        popup = MessageBoxComponent(
            self.master,
            title=title,
            message=message,
            width=400,
            height=200,
            modal=True
        )
        popup.show()

   # def _clear_fields(self):
        # self.username_field.input_widget.delete(0, tk.END)
         # self.password_field.input_widget.delete(0, tk.END)
    def _clear_fields(self):
        self.username_field.set_value("")
        self.password_field.set_value("")

