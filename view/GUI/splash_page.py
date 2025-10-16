from tkinter import Frame
from components.label_component import LabelComponent
from components.progress_bar_component import ProgressBarComponent
from view.GUI.base_page import BasePage
from resources.parameters.app_parameters import SPLASH_CONFIG


class SplashScreenPage(BasePage):
    def __init__(self, master, on_finish):
        super().__init__(master)
        self._on_finish = on_finish
        self.set_background_color(SPLASH_CONFIG["background_color"])

        self.center_frame = Frame(self, bg=self["bg"])
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label = None
        self.progress = None

        self.create_component()
        self.render()

        self.after(2000, self.finish_splash)

    def create_component(self):
        self.label = LabelComponent(
            self.center_frame,
            text=SPLASH_CONFIG["label_text"],
            style=SPLASH_CONFIG["label_style"],
            layout="pack",
            padding=SPLASH_CONFIG["label_padding"]
        )

        self.progress = ProgressBarComponent(
            self.center_frame,
            length=SPLASH_CONFIG["progress_length"],
            step=SPLASH_CONFIG["progress_step"],
            interval=SPLASH_CONFIG["progress_interval"],
            autostart=SPLASH_CONFIG["progress_autostart"],
            layout=SPLASH_CONFIG["progress_layout"],
            padding=SPLASH_CONFIG["progress_padding"]
        )

    def render(self):
        self.label.render()
        self.progress.render()

    def finish_splash(self):
        self._on_finish()
