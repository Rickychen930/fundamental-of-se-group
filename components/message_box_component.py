import tkinter as tk
from .component import Component
from resources.parameters.app_parameters import MESSAGEBOX_CONFIG

class MessageBoxComponent:
    def __init__(
        self,
        master,
        title=None,
        message=None,
        width=400,
        height=200,
        modal=True,
        **kwargs
    ):
        self._title = title or MESSAGEBOX_CONFIG.get("default_title", "Notice")
        self._message = message or ""
        self._width = width
        self._height = height
        self._modal = modal
        self.master = master

        self.window = None
        self.title_label = None
        self.message_label = None

        self._create_popup()

    def _create_popup(self):
        self.window = tk.Toplevel(self.master)
        self.window.title(self._title)
        self.window.geometry(f"{self._width}x{self._height}")
        self.window.configure(bg=MESSAGEBOX_CONFIG.get("background_color", "#f0f0f0"))
        self.window.resizable(False, False)

        if self._modal:
            self.window.transient(self.master)
            self.window.grab_set()

        # Title label
        self.title_label = tk.Label(
            self.window,
            text=self._title,
            font=MESSAGEBOX_CONFIG.get("title_font", ("Helvetica", 14, "bold")),
            fg=MESSAGEBOX_CONFIG.get("title_fg", "#333"),
            bg=MESSAGEBOX_CONFIG.get("background_color", "#f0f0f0")
        )
        self.title_label.pack(pady=(20, 10))

        # Message label
        self.message_label = tk.Label(
            self.window,
            text=self._message,
            font=MESSAGEBOX_CONFIG.get("message_font", ("Helvetica", 11)),
            fg=MESSAGEBOX_CONFIG.get("message_fg", "#555"),
            bg=MESSAGEBOX_CONFIG.get("background_color", "#f0f0f0"),
            wraplength=self._width - 40,
            justify=MESSAGEBOX_CONFIG.get("justify", "left")
        )
        self.message_label.pack(pady=(0, 20), padx=20)

        # OK button
        ok_button = tk.Button(
            self.window,
            text=MESSAGEBOX_CONFIG.get("ok_text", "OK"),
            command=self.window.destroy
        )
        ok_button.pack(pady=(0, 10))

    def set_message(self, message):
        self._message = message
        if self.message_label:
            self.message_label.config(text=message)

    def set_title(self, title):
        self._title = title
        if self.title_label:
            self.title_label.config(text=title)
            self.window.title(title)

    def show(self):
        self.window.deiconify()

    def hide(self):
        self.window.withdraw()
