from tkinter import Frame
from components.label_component import LabelComponent
from components.progress_bar_component import ProgressBarComponent
from view.GUI.base_page import BasePage
from resources.parameters.app_parameters import SPLASH_CONFIG

class SplashScreenPage(BasePage):
    """
    SplashScreenPage displays a temporary welcome screen with a label and progress bar.
    After a short delay, it triggers a callback to continue to the next page.
    """

    def __init__(self, master, on_continue):
        """
        Initialize splash screen with background, centered content, and timed transition.

        Args:
            master (tk.Tk or tk.Frame): Parent container.
            on_continue (callable): Function to call after splash delay.
        """
        super().__init__(master)
        self._on_continue = on_continue
        self.set_background_color(SPLASH_CONFIG["background_color"])

        self._setup_layout()
        self._create_components()
        self._render_components()

        # Trigger transition after delay (e.g. 2 seconds)
        self.after(2000, self._finish_splash)

    def _setup_layout(self):
        """Create and center the frame that holds splash content."""
        self.center_frame = Frame(self, bg=self["bg"])
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

    def _create_components(self):
        """Initialize label and progress bar components using config."""
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

    def _render_components(self):
        """Render splash label and progress bar."""
        self.label.render()
        self.progress.render()

    def _finish_splash(self):
        """Invoke continuation callback after splash delay."""
        if callable(self._on_continue):
            self._on_continue()
