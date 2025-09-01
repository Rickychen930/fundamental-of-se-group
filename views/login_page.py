from tkinter import Frame
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

        config = LOGIN_CONFIG
        self.set_background_color(config["background_color"])
        self.set_title(
            config["title_text"],
            font=config["title_font"],
            pady=config["title_padding"]
        )

        # Frame tengah
        self.center_frame = self.add_centered_frame()

        # Form container
        self.form_frame = Frame(self.center_frame, bg=self["bg"])
        self.form_frame.pack(
            pady=config["form_padding_y"],
            padx=config["form_padding_x"],
            fill="x"
        )

        self.username_field = FormField(
            self.form_frame,
            label_text=config["username_label"],
            label_style=config["field_label_style"],
            label_font=config["field_label_font"],
            input_width=config["input_width"],
            input_font=config["input_font"],
            input_fg=config["input_fg"],
            input_bg=config["input_bg"],
            padding=config["input_padding"],
            autoselect=True
        )

        self.password_field = FormField(
            self.form_frame,
            label_text=config["password_label"],
            label_style=config["field_label_style"],
            label_font=config["field_label_font"],
            input_width=config["input_width"],
            input_font=config["input_font"],
            input_fg=config["input_fg"],
            input_bg=config["input_bg"],
            padding=config["input_padding"]
        )

        # Button container
        self.button_frame = Frame(self.center_frame, bg=self["bg"])
        self.button_frame.pack(pady=config["button_frame_padding"])

        self.login_button = ButtonComponent(
            self.button_frame,
            name=config["button_text"],
            action=self.handle_login,
            style=config["button_style"],
            layout=config["button_layout"],
            padding=config["button_padding"]
        )

        self.create_components()
        self.render()

    def create_components(self):
        self.username_field.create_component()
        self.password_field.create_component()
        self.login_button.create_component()

    def render(self):
        self.username_field.render()
        self.password_field.render()
        self.login_button.render()

    def handle_login(self):
        username = self.username_field.get_value()
        password = self.password_field.get_value()
        print(f"Username: {username}, Password: {password}")
