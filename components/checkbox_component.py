import tkinter as tk
from .component import Component
from resources.parameters.app_parameters import CHECKBOX_CONFIG

class CheckboxComponent(Component):
    """
    CheckboxComponent wraps a styled tk.Checkbutton with layout and state control.
    Useful for toggles, preferences, and form inputs.
    """

    def __init__(
        self,
        master,
        text,
        checked=False,
        layout=None,
        padding=None,
        **kwargs
    ):
        """
        Initialize the checkbox component.

        Args:
            master (tk.Widget): Parent widget.
            text (str): Label text for the checkbox.
            checked (bool): Initial checked state.
            layout (str): Layout manager ('pack', 'grid', 'place').
            padding (tuple): (padx, pady) values.
            **kwargs: Additional configuration passed to base Component.
        """
        super().__init__(
            master,
            layout=layout or CHECKBOX_CONFIG["layout"],
            padding=padding or CHECKBOX_CONFIG["padding"],
            **kwargs
        )
        self._text = text
        self._var = tk.BooleanVar(value=checked)
        self._checkbox = None

        self.create_component()

    def create_component(self):
        """Create the internal tk.Checkbutton widget with styling and configuration."""
        self._checkbox = tk.Checkbutton(
            self.get_root(),
            text=self._text,
            variable=self._var,
            font=CHECKBOX_CONFIG["font"],
            fg=CHECKBOX_CONFIG["fg"],
            bg=CHECKBOX_CONFIG["bg"],
            anchor="w"
        )

    def render(self):
        """Render the checkbox using the specified layout manager."""
        if not self._checkbox:
            return

        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._checkbox.pack(padx=padx, pady=pady, anchor="w")
        elif layout == "grid":
            self._checkbox.grid(padx=padx, pady=pady, sticky="w")
        elif layout == "place":
            self._checkbox.place(relx=0.5, rely=0.5, anchor="center")

    def is_checked(self):
        """
        Check whether the checkbox is selected.

        Returns:
            bool: True if checked, False otherwise.
        """
        return self._var.get()

    def set_checked(self, value: bool):
        """
        Set the checkbox state.

        Args:
            value (bool): True to check, False to uncheck.
        """
        self._var.set(value)

    def get_widget(self):
        """
        Access the internal checkbox widget.

        Returns:
            tk.Checkbutton: The rendered checkbox instance.
        """
        return self._checkbox
