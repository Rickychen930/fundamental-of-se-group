from .component import Component
from resources.parameters.app_parameters import LABEL_CONFIG

class LabelComponent(Component):
    """
    LabelComponent wraps a styled ttk.Label with layout and padding control.
    Supports both static text and dynamic textvariable binding.
    """

    def __init__(
        self,
        master,
        text=None,
        textvariable=None,
        style=None,
        font=None,
        fg=None,
        bg=None,
        layout=None,
        padding=None,
        **kwargs
    ):
        """
        Initialize the label component.

        Args:
            master (tk.Widget): Parent widget.
            text (str, optional): Static text to display.
            textvariable (tk.StringVar, optional): Variable for dynamic text binding.
            style (str, optional): ttk style name.
            font (tuple, optional): Font tuple.
            fg (str, optional): Foreground (text) color.
            bg (str, optional): Background color.
            layout (str, optional): Layout manager ('pack', 'grid', 'place').
            padding (tuple, optional): (padx, pady) values.
            **kwargs: Additional configuration passed to base Component.
        """
        super().__init__(
            master,
            style=style or LABEL_CONFIG["style"],
            font=font or LABEL_CONFIG["font"],
            fg=fg or LABEL_CONFIG["fg"],
            bg=bg or LABEL_CONFIG["bg"],
            layout=layout or LABEL_CONFIG["layout"],
            padding=padding or LABEL_CONFIG["padding"],
            **kwargs
        )
        self._text = text
        self._textvariable = textvariable
        self._label = None
        self.label_widget = None

        self.create_component()

    def create_component(self):
        """Create the internal ttk.Label widget with styling and configuration."""
        config = {
            "style": self.get_style()
        }

        if self._text is not None:
            config["text"] = self._text
        if self._textvariable is not None:
            config["textvariable"] = self._textvariable
        if self.get_font():
            config["font"] = self.get_font()
        if self.get_foreground():
            config["foreground"] = self.get_foreground()
        if self.get_background_color():
            config["background"] = self.get_background_color()

        config.update(self.get_extra())
        self._label = self.get_ttk().Label(self.get_root(), **config)
        self.label_widget = self._label

    def render(self):
        """
        Render the label using the specified layout manager.

        Returns:
            ttk.Label: The rendered label widget.
        """
        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._label.pack(padx=padx, pady=pady)
        elif layout == "grid":
            self._label.grid(padx=padx, pady=pady)
        elif layout == "place":
            self._label.place(relx=0.5, rely=0.5, anchor="center")

        return self._label

    def get_widget(self):
        """
        Access the internal label widget.

        Returns:
            ttk.Label: The label instance.
        """
        return self._label
