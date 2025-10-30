from tkinter import Tk, messagebox
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
    """
    Main application class that manages window initialization, page navigation,
    controller injection, and lifecycle management.
    """

    def __init__(self):
        """Initialize the application window, styles, controllers, and load splash screen."""
        self.root = Tk()
        self._initialize_window()
        setup_styles()

        # Initialize shared resources
        self.db = Database()
        self.student_controller = StudentController(self.db)
        self.admin_controller = AdminController(self.db)

        # Page registry
        self.pages = {
            "splash": SplashScreenPage,
            "login": LoginPage,
            "enrolment": EnrolmentPage,
            # "admin": AdminPage,  # Add if needed
        }

        self.current_page = None
        self.navigate("splash")

    def _initialize_window(self):
        """Configure main window properties."""
        self.root.title(APP_CONFIG.get("title", "University App"))
        self.root.configure(bg=APP_CONFIG.get("background_color", "#FFFFFF"))
        self.root.resizable(False, False)

    def navigate(self, page_name: str):
        """
        Navigate to a registered page by name.

        Args:
            page_name (str): Key name of the page in self.pages
        """
        self._clear_current_page()

        page_class = self.pages.get(page_name)
        if not page_class:
            self._show_error(f"Page '{page_name}' not found.")
            return

        # Dynamically prepare constructor arguments
        kwargs = {"master": self.root}
        sig = inspect.signature(page_class.__init__)

        if "controller" in sig.parameters:
            kwargs["controller"] = (
                self.admin_controller if page_name == "admin" else self.student_controller
            )
        if "app" in sig.parameters:
            kwargs["app"] = self
        if "db" in sig.parameters:
            kwargs["db"] = self.db
        if page_name == "splash" and "on_continue" in sig.parameters:
            kwargs["on_continue"] = lambda: self.navigate("login")

        try:
            self.current_page = page_class(**kwargs)
            self.current_page.pack(fill="both", expand=True)

            # Optional render hook
            if hasattr(self.current_page, "render") and callable(self.current_page.render):
                self.current_page.render()

            self._resize_window()
        except Exception as e:
            self._show_error(f"Failed to load page '{page_name}': {e}")

    def _resize_window(self):
        """Resize window to fit current page content with minimum dimensions."""
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        min_width = max(width, 700)
        min_height = max(height, 400)
        self.root.geometry(f"{min_width}x{min_height}+100+100")

    def _clear_current_page(self):
        """Remove the current page from view and destroy its instance."""
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()
            self.current_page = None

    def _show_error(self, message):
        """Display an error message in a modal dialog."""
        messagebox.showerror("Navigation Error", message)

    def run(self):
        """Start the main application loop."""
        self.root.mainloop()
