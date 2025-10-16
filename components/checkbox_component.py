# components/checkbox_component.py
import tkinter as tk
from .component import Component
from resources.parameters.app_parameters import CHECKBOX_CONFIG

class CheckboxComponent(Component):
    def __init__(
        self,
        master,
        text,
        checked=False,
        layout=None,
        padding=None,
        **kwargs
    ):
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
        layout = self.get_layout()
        padx, pady = self.get_padding()
        if layout == "pack":
            self._checkbox.pack(padx=padx, pady=pady, anchor="w")
        elif layout == "grid":
            self._checkbox.grid(padx=padx, pady=pady, sticky="w")
        elif layout == "place":
            self._checkbox.place(relx=0.5, rely=0.5, anchor="center")

    def is_checked(self):
        return self._var.get()

    def set_checked(self, value: bool):
        self._var.set(value)

    def get_widget(self):
        return self._checkbox
