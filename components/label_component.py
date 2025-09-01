from .component import Component
from resources.parameters.app_parameters import LABEL_CONFIG

class LabelComponent(Component):
    def __init__(
        self,
        master,
        text,
        style=None,
        font=None,
        fg=None,
        bg=None,
        layout=None,
        padding=None,
        **kwargs
    ):
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
        self._label = None
        self.create_component()

    def create_component(self):
        config = {
            "text": self._text,
            "style": self.get_style()
        }

        if self.get_font(): config["font"] = self.get_font()
        if self.get_foreground(): config["foreground"] = self.get_foreground()
        if self.get_background_color(): config["background"] = self.get_background_color()

        config.update(self.get_extra())
        self._label = self.get_ttk().Label(self.get_root(), **config)

    def render(self):
        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._label.pack(padx=padx, pady=pady)
        elif layout == "grid":
            self._label.grid(padx=padx, pady=pady)
        elif layout == "place":
            self._label.place(relx=0.5, rely=0.5, anchor="center")
