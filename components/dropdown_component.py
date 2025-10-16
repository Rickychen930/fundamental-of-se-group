# components/dropdown_component.py
import tkinter as tk
from tkinter import ttk
from .component import Component
from resources.parameters.app_parameters import DROPDOWN_CONFIG

class DropdownComponent(Component):
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
        self._dropdown = ttk.Combobox(
            self.get_root(),
            textvariable=self._var,
            values=self._values,
            width=self._width,
            state="readonly"
        )

    def render(self):
        layout = self.get_layout()
        padx, pady = self.get_padding()
        if layout == "pack":
            self._dropdown.pack(padx=padx, pady=pady)
        elif layout == "grid":
            self._dropdown.grid(padx=padx, pady=pady)
        elif layout == "place":
            self._dropdown.place(relx=0.5, rely=0.5, anchor="center")

    def get_value(self):
        return self._var.get()

    def set_value(self, value):
        self._var.set(value)

    def get_widget(self):
        return self._dropdown
