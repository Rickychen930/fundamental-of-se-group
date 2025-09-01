from .component import Component
import tkinter as tk
from resources.parameters.app_parameters import TEXT_INPUT_CONFIG

class TextInputComponent(Component):
    def __init__(
        self,
        master,
        height=None,
        width=None,
        font=None,
        fg=None,
        bg=None,
        bd=None,
        relief=None,
        layout=None,
        padding=None,
        autoselect=None,
        **kwargs
    ):
        super().__init__(
            master,
            font=font or TEXT_INPUT_CONFIG["font"],
            fg=fg or TEXT_INPUT_CONFIG["fg"],
            bg=bg or TEXT_INPUT_CONFIG["bg"],
            layout=layout or TEXT_INPUT_CONFIG["layout"],
            padding=padding or TEXT_INPUT_CONFIG["padding"],
            **kwargs
        )
        self._height = height if height is not None else TEXT_INPUT_CONFIG["height"]
        self._width = width if width is not None else TEXT_INPUT_CONFIG["width"]
        self._bd = bd if bd is not None else TEXT_INPUT_CONFIG["bd"]
        self._relief = relief if relief is not None else TEXT_INPUT_CONFIG["relief"]
        self._autoselect = autoselect if autoselect is not None else TEXT_INPUT_CONFIG["autoselect"]
        self._text_box = None

        self.create_component()

    def create_component(self):
        config = {
            "height": self._height,
            "width": self._width,
            "font": self.get_font(),
            "bg": self.get_background_color(),
            "fg": self.get_foreground(),
            "bd": self._bd,
            "relief": self._relief
        }
        config.update(self.get_extra())

        self._text_box = tk.Text(self.get_root(), **config)

    def render(self):
        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self._text_box.pack(fill="x", padx=padx, pady=(0, pady))
        elif layout == "grid":
            self._text_box.grid(padx=padx, pady=(0, pady))
        elif layout == "place":
            self._text_box.place(relx=0.5, rely=0.5, anchor="center")

        if self._autoselect:
            self._text_box.focus_set()

    def get_text(self) -> str:
        if self._text_box:
            return self._text_box.get("1.0", tk.END).strip()
        return ""

    def set_text(self, value: str):
        if self._text_box:
            self._text_box.delete("1.0", tk.END)
            self._text_box.insert("1.0", value)
