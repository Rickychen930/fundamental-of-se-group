# components/radio_group_component.py
import tkinter as tk
from .component import Component
from resources.parameters.app_parameters import RADIO_CONFIG

class RadioGroupComponent(Component):
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
        padx, pady = self.get_padding()
        for i, btn in enumerate(self._buttons):
            if self._orientation == "vertical":
                btn.grid(row=i, column=0, padx=padx, pady=pady, sticky="w")
            else:
                btn.grid(row=0, column=i, padx=padx, pady=pady)

    def get_value(self):
        return self._var.get()

    def set_value(self, value):
        self._var.set(value)

    def get_widgets(self):
        return self._buttons
