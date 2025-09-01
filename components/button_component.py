from .component import Component
from resources.parameters.app_parameters import BUTTON_CONFIG

class ButtonComponent(Component):
    def __init__(
        self,
        master,
        name,
        action,
        style=None,
        padding=None,
        layout=None,
        **kwargs
    ):
        config = BUTTON_CONFIG
        super().__init__(
            master,
            style=style or config["style"],
            padding=padding or config["padding"],
            layout=layout or config["layout"],
            **kwargs
        )
        self._name = name
        self._action = action
        self._btn = None

    def create_component(self):
        config = {
            "text": self._name,
            "command": self._action,
            "style": self.get_style()
        }
        config.update(self.get_extra())

        self._btn = self.get_ttk().Button(self.get_root(), **config)

    def render(self):
        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._btn.pack(ipadx=padx, ipady=pady)
        elif layout == "grid":
            self._btn.grid(padx=padx, pady=pady)
        elif layout == "place":
            self._btn.place(relx=0.5, rely=0.5, anchor="center")
