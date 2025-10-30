import tkinter as tk
from .component import Component
from resources.parameters.app_parameters import TEXT_INPUT_CONFIG

class TextInputComponent(Component):
    """
    TextInputComponent wraps a styled tk.Entry widget with layout, padding, and value control.
    Supports password masking, auto-focus, and dynamic text access.
    """

    def __init__(
        self,
        master,
        width=None,
        font=None,
        fg=None,
        bg=None,
        bd=None,
        relief=None,
        layout=None,
        padding=None,
        autoselect=None,
        show=None,
        **kwargs
    ):
        """
        Initialize the text input component.

        Args:
            master (tk.Widget): Parent widget.
            width (int, optional): Width of the input field in characters.
            font (tuple, optional): Font tuple (family, size, weight).
            fg (str, optional): Foreground (text) color.
            bg (str, optional): Background color.
            bd (int, optional): Border width.
            relief (str, optional): Relief style ('flat', 'sunken', etc.).
            layout (str, optional): Layout manager ('pack', 'grid', 'place').
            padding (tuple, optional): (padx, pady) values.
            autoselect (bool, optional): Whether to auto-focus the input field.
            show (str, optional): Mask character for password fields (e.g., '*').
            **kwargs: Additional configuration passed to base Component.
        """
        super().__init__(
            master,
            font=font or TEXT_INPUT_CONFIG["font"],
            fg=fg or TEXT_INPUT_CONFIG["fg"],
            bg=bg or TEXT_INPUT_CONFIG["bg"],
            layout=layout or TEXT_INPUT_CONFIG["layout"],
            padding=padding or TEXT_INPUT_CONFIG["padding"],
            **kwargs
        )

        self._width = width or TEXT_INPUT_CONFIG["width"]
        self._bd = bd if bd is not None else TEXT_INPUT_CONFIG["bd"]
        self._relief = relief or TEXT_INPUT_CONFIG["relief"]
        self._autoselect = autoselect if autoselect is not None else TEXT_INPUT_CONFIG["autoselect"]
        self._show = show

        self._var = tk.StringVar()
        self._entry = None

        self.create_component()

    def create_component(self):
        """Create the internal tk.Entry widget with styling and configuration."""
        config = {
            "textvariable": self._var,
            "width": self._width,
            "font": self.get_font(),
            "bg": self.get_background_color(),
            "fg": self.get_foreground(),
            "bd": self._bd,
            "relief": self._relief
        }

        if self._show:
            config["show"] = self._show

        config.update(self.get_extra())
        self._entry = tk.Entry(self.get_root(), **config)

    def render(self):
        """Render the input field using the specified layout manager."""
        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._entry.pack(fill="x", padx=padx, pady=(0, pady))
        elif layout == "grid":
            self._entry.grid(padx=padx, pady=(0, pady))
        elif layout == "place":
            self._entry.place(relx=0.5, rely=0.5, anchor="center")

        if self._autoselect:
            self._entry.focus_set()

    def get_text(self) -> str:
        """
        Get the current text value from the input field.

        Returns:
            str: Text entered by the user.
        """
        return self._var.get()

    def set_text(self, value: str):
        """
        Set the text value of the input field.

        Args:
            value (str): Text to populate in the field.
        """
        self._var.set(value)

    def get_widget(self):
        """
        Access the internal tk.Entry widget.

        Returns:
            tk.Entry: The entry widget instance.
        """
        return self._entry
