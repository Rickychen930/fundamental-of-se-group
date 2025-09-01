from tkinter import Tk
from views.login_page import LoginPage
from views.splash_page import SplashScreenPage
from theme.style_config import setup_styles
from resources.parameters.app_parameters import APP_CONFIG

class MainPage:
    def __init__(self):
        self.root = Tk()
        self._init_window()
        setup_styles()

        self.current_page = None
        self.show_splash()

    def _init_window(self):
        self.root.title(APP_CONFIG["title"])
        self.root.geometry(APP_CONFIG["geometry"])
        self.root.configure(bg=APP_CONFIG["background_color"])

    def show_splash(self):
        self._clear_current_page()
        self.current_page = SplashScreenPage(self.root, self.show_login_page)
        self.current_page.pack(fill="both", expand=True)

    def show_login_page(self):
        self._clear_current_page()
        self.current_page = LoginPage(self.root, self)
        self.current_page.pack(fill="both", expand=True)
        self.current_page.render()

    def _clear_current_page(self):
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()
            self.current_page = None

    def run(self):
        self.root.mainloop()

main = MainPage()
main.run()
