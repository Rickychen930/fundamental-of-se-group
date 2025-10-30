import tkinter as tk
from .component import Component
from resources.parameters.app_parameters import RADIO_CONFIG

class RadioGroupComponent(Component):
    """
    RadioGroupComponent creates a group of radio buttons with shared selection logic.
    Supports vertical or horizontal layout and dynamic value access.
    """

    def __init__(
        self,
        master,
        options,
        default=None,
        layout=None,
        padding=None,
        orientation="vertical",
        **kwargs
    ):
        """
        Initialize the radio group component.

        Args:
            master (tk.Widget): Parent widget.
            options (list): List of string options to display as radio buttons.
            default (str, optional): Default selected option.
            layout (str, optional): Layout manager ('pack', 'grid', 'place').
            padding (tuple, optional): (padx, pady) values.
            orientation (str): 'vertical' or 'horizontal' layout.
            **kwargs: Additional configuration passed to base Component.
        """
        super().__init__(
            master,
            layout=layout or RADIO_CONFIG["layout"],
            padding=padding or RADIO_CONFIG["padding"],
            **kwargs
        )
        self._options = options
        self._default = default or (options[0] if options else "")
        self._orientation = orientation
        self._var = tk.StringVar(value=self._default)
        self._buttons = []

        self.create_component()

    def create_component(self):
        """Create radio buttons for each option."""
        for option in self._options:
            btn = tk.Radiobutton(
                self.get_root(),
                text=option,
                variable=self._var,
                value=option,
                font=RADIO_CONFIG["font"],
                fg=RADIO_CONFIG["fg"],
                bg=RADIO_CONFIG["bg"],
                anchor="w"
            )
            self._buttons.append(btn)

    def render(self):
        """Render radio buttons using the specified orientation and layout."""
        padx, pady = self.get_padding()
        for i, btn in enumerate(self._buttons):
            if self._orientation == "vertical":
                btn.grid(row=i, column=0, padx=padx, pady=pady, sticky="w")
            else:
                btn.grid(row=0, column=i, padx=padx, pady=pady)

    def get_value(self):
        """
        Get the currently selected option.

        Returns:
            str: Selected radio button value.
        """
        return self._var.get()

    def set_value(self, value):
        """
        Set the selected option programmatically.

        Args:
            value (str): Option to select.
        """
        self._var.set(value)

    def get_widgets(self):
        """
        Get the list of radio button widgets.

        Returns:
            list[tk.Radiobutton]: All radio buttons in the group.
        """
        return self._buttons
