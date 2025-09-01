from tkinter import *
from tkinter import ttk
from resources.parameters.app_parameters import COMPONENT_DEFAULTS

class Component:
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
        self._master = master
        self._ttk = ttk
        self._style = style if style is not None else COMPONENT_DEFAULTS["style"]
        self._font = font if font is not None else COMPONENT_DEFAULTS["font"]
        self._fg = fg if fg is not None else COMPONENT_DEFAULTS["foreground"]
        self._bg = bg if bg is not None else self._resolve_background()
        self._padding = padding if padding is not None else COMPONENT_DEFAULTS["padding"]
        self._layout = layout if layout is not None else COMPONENT_DEFAULTS["layout"]
        self._extra = kwargs

    def get_root(self):
        return self._master

    def get_ttk(self):
        return self._ttk

    def get_background_color(self):
        return self._bg

    def get_style(self):
        return self._style

    def get_font(self):
        return self._font

    def get_foreground(self):
        return self._fg

    def get_layout(self):
        return self._layout

    def get_padding(self):
        return self._padding

    def get_extra(self):
        return self._extra

    def _resolve_background(self):
        try:
            return COMPONENT_DEFAULTS["background"]
        except (KeyError, TclError):
            return "#f0f0f0"
