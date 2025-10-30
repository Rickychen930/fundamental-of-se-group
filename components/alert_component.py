from .component import Component
from resources.parameters.app_parameters import ALERT_CONFIG

class AlertComponent(Component):
    """
    AlertComponent displays a styled message label with optional visibility control.
    Useful for showing warnings, tips, or status messages in forms and pages.
    """

    def __init__(
        self,
        master,
        message=None,
        style=None,
        layout=None,
        padding=None,
        visible=True,
        **kwargs
    ):
        """
        Initialize the alert component.

        Args:
            master (tk.Widget): Parent widget.
            message (str): Initial message to display.
            style (str): ttk style name.
            layout (str): Layout manager ('pack', 'grid', 'place').
            padding (tuple): (padx, pady) values.
            visible (bool): Whether the alert is initially visible.
            **kwargs: Additional configuration passed to the base Component.
        """
        super().__init__(
            master,
            style=style or ALERT_CONFIG["style"],
            layout=layout or ALERT_CONFIG["layout"],
            padding=padding or ALERT_CONFIG["padding"],
            **kwargs
        )
        self._message = message or ""
        self._visible = visible
        self.label = None

        self.create_component()

    def create_component(self):
        """Create the internal label widget with styling and configuration."""
        config = {
            "text": self._message,
            "style": self.get_style(),
            "wraplength": ALERT_CONFIG.get("wraplength", 400),
            "justify": ALERT_CONFIG.get("justify", "left")
        }
        config.update(self.get_extra())
        self.label = self.get_ttk().Label(self.get_root(), **config)

    def render(self):
        """Render the label using the specified layout if visible."""
        if not self._visible or not self.label:
            return

        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self.label.pack(padx=padx, pady=pady, anchor="w")
        elif layout == "grid":
            self.label.grid(padx=padx, pady=pady, sticky="w")
        elif layout == "place":
            self.label.place(relx=0.5, rely=0.5, anchor="center")

    def set_message(self, message):
        """
        Update the alert message.

        Args:
            message (str): New message to display.
        """
        self._message = message
        if self.label:
            self.label.config(text=message)

    def hide(self):
        """Hide the alert label from view."""
        self._visible = False
        if self.label:
            self.label.pack_forget()
            self.label.grid_forget()
            self.label.place_forget()

    def show(self):
        """Show the alert label if hidden."""
        self._visible = True
        self.render()
