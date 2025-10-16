from tkinter import Tk
from view.GUI.login_page import LoginPage
from view.GUI.splash_page import SplashScreenPage
from view.GUI.enrolment_page import EnrolmentPage

from theme.style_config import setup_styles
from resources.parameters.app_parameters import APP_CONFIG
from db.database import Database
from controller.student_controller import StudentController
from controller.admin_controller import AdminController
import inspect

class App:
    def __init__(self):
        self.root = Tk()
        self._initialize_window()
        setup_styles()

        # Initialize database and controllers
        self.db = Database()
        self.student_controller = StudentController(self.db)
        self.admin_controller = AdminController(self.db)

        # Page registry
        self.pages = {
            "splash": SplashScreenPage,
            "login": LoginPage,
            "enrolment": EnrolmentPage,
        }

        self.current_page = None
        self.navigate("splash")

    def _initialize_window(self):
        self.root.title(APP_CONFIG.get("title", "University App"))
        self.root.configure(bg=APP_CONFIG.get("background_color", "#FFFFFF"))
        self.root.resizable(False, False)

    def navigate(self, page_name: str):
        self._clear_current_page()

        page_class = self.pages.get(page_name)
        if not page_class:
            self._show_error(f"Page '{page_name}' not found.")
            return

        # Prepare arguments based on constructor signature
        kwargs = {"master": self.root}
        sig = inspect.signature(page_class.__init__)
        if "controller" in sig.parameters:
            kwargs["controller"] = self.student_controller if page_name != "admin" else self.admin_controller
        if "app" in sig.parameters:
            kwargs["app"] = self
        if "db" in sig.parameters:
            kwargs["db"] = self.db
        if page_name == "splash" and "on_continue" in sig.parameters:
            kwargs["on_continue"] = lambda: self.navigate("login")

        try:
            self.current_page = page_class(**kwargs)
            self.current_page.pack(fill="both", expand=True)

            if hasattr(self.current_page, "render") and callable(self.current_page.render):
                self.current_page.render()

            self._resize_window()
        except Exception as e:
            self._show_error(f"Failed to load page '{page_name}': {e}")

    def _resize_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        min_width = max(width, 700)
        min_height = max(height, 400)
        self.root.geometry(f"{min_width}x{min_height}+100+100")

    def _clear_current_page(self):
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()
            self.current_page = None

    def _show_error(self, message):
        from tkinter import messagebox
        messagebox.showerror("Navigation Error", message)

    def run(self):
        self.root.mainloop()
