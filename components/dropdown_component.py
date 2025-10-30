import tkinter as tk
from tkinter import ttk
from .component import Component
from resources.parameters.app_parameters import DROPDOWN_CONFIG

class DropdownComponent(Component):
    """
    DropdownComponent wraps a styled ttk.Combobox with layout and value control.
    Useful for selection inputs in forms, filters, and configuration panels.
    """

    def __init__(
        self,
        master,
        values=None,
        default=None,
        style=None,
        layout=None,
        padding=None,
        width=None,
        **kwargs
    ):
        """
        Initialize the dropdown component.

        Args:
            master (tk.Widget): Parent widget.
            values (list): List of selectable string options.
            default (str): Default selected value.
            style (str): ttk style name.
            layout (str): Layout manager ('pack', 'grid', 'place').
            padding (tuple): (padx, pady) values.
            width (int): Width of the dropdown in characters.
            **kwargs: Additional configuration passed to base Component.
        """
        super().__init__(
            master,
            style=style or DROPDOWN_CONFIG["style"],
            layout=layout or DROPDOWN_CONFIG["layout"],
            padding=padding or DROPDOWN_CONFIG["padding"],
            **kwargs
        )
        self._values = values or []
        self._default = default or (self._values[0] if self._values else "")
        self._width = width or DROPDOWN_CONFIG.get("width", 20)
        self._var = tk.StringVar(value=self._default)
        self._dropdown = None

        self.create_component()

    def create_component(self):
        """Create the internal ttk.Combobox widget with configured options."""
        self._dropdown = ttk.Combobox(
            self.get_root(),
            textvariable=self._var,
            values=self._values,
            width=self._width,
            state="readonly"
        )

    def render(self):
        """Render the dropdown using the specified layout manager."""
        if not self._dropdown:
            return

        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._dropdown.pack(padx=padx, pady=pady)
        elif layout == "grid":
            self._dropdown.grid(padx=padx, pady=pady)
        elif layout == "place":
            self._dropdown.place(relx=0.5, rely=0.5, anchor="center")

    def get_value(self):
        """
        Get the currently selected value.

        Returns:
            str: Selected value from the dropdown.
        """
        return self._var.get()

    def set_value(self, value):
        """
        Set the selected value in the dropdown.

        Args:
            value (str): Value to select.
        """
        self._var.set(value)

    def get_widget(self):
        """
        Access the internal dropdown widget.

        Returns:
            ttk.Combobox: The rendered dropdown instance.
        """
        return self._dropdown
