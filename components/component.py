from tkinter import TclError
from tkinter import ttk

from resources.parameters.app_parameters import COMPONENT_DEFAULTS

class Component:
    """
    Base class for all GUI components.
    Provides consistent styling, layout, and configuration access across custom widgets.
    """

    def __init__(
        self,
        master,
        style=None,
        font=None,
        fg=None,
        bg=None,
        padding=None,
        layout=None,
        **kwargs
    ):
        """
        Initialize the component with styling and layout configuration.

        Args:
            master (tk.Widget): Parent widget.
            style (str): ttk style name.
            font (tuple): Font tuple (family, size, weight).
            fg (str): Foreground (text) color.
            bg (str): Background color.
            padding (tuple): (padx, pady) values.
            layout (str): Layout manager ('pack', 'grid', 'place').
            **kwargs: Additional configuration passed to child widgets.
        """
        self._master = master
        self._ttk = ttk

        # Resolve configuration with fallback to defaults
        self._style = style or COMPONENT_DEFAULTS.get("style")
        self._font = font or COMPONENT_DEFAULTS.get("font")
        self._fg = fg or COMPONENT_DEFAULTS.get("foreground")
        self._bg = bg or self._resolve_background()
        self._padding = padding or COMPONENT_DEFAULTS.get("padding")
        self._layout = layout or COMPONENT_DEFAULTS.get("layout")
        self._extra = kwargs

    # Accessors
    def get_root(self):
        """Return the parent widget."""
        return self._master

    def get_ttk(self):
        """Return the ttk module reference."""
        return self._ttk

    def get_background_color(self):
        """Return the resolved background color."""
        return self._bg

    def get_style(self):
        """Return the resolved ttk style name."""
        return self._style

    def get_font(self):
        """Return the resolved font tuple."""
        return self._font

    def get_foreground(self):
        """Return the resolved foreground color."""
        return self._fg

    def get_layout(self):
        """Return the layout manager type."""
        return self._layout

    def get_padding(self):
        """Return the (padx, pady) padding tuple."""
        return self._padding

    def get_extra(self):
        """Return any additional keyword arguments."""
        return self._extra

    def _resolve_background(self):
        """
        Safely resolve background color from defaults.

        Returns:
            str: Background color string.
        """
        try:
            return COMPONENT_DEFAULTS["background"]
        except (KeyError, TclError):
            return "#f0f0f0"  # Fallback to light gray
