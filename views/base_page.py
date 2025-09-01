from tkinter import *
from tkinter import ttk
from resources.parameters.app_parameters import PAGE_CONFIG

class BasePage(Frame):
    def __init__(self, master, bg=None, layout="pack", **kwargs):
        bg = bg or PAGE_CONFIG["default_bg"]
        super().__init__(master, bg=bg, **kwargs)
        self.master = master
        self.ttk = ttk
        self.title_label = None
        self._layout = layout

        # Default layout
        if self._layout == "pack":
            self.pack(fill=BOTH, expand=True)
        elif self._layout == "grid":
            self.grid(sticky="nsew")
        elif self._layout == "place":
            self.place(relx=0.5, rely=0.5, anchor="center")

    def clear_page(self):
        for widget in self.winfo_children():
            if widget != self.title_label:
                widget.destroy()

    def set_background_color(self, color=None):
        self.configure(bg=color or PAGE_CONFIG["default_bg"])

    def set_title(
        self,
        text,
        style=None,
        font=None,
        fg=None,
        bg=None,
        pady=None,
        anchor=None
    ):
        style = style or PAGE_CONFIG["title_style"]
        font = font or PAGE_CONFIG["title_font"]
        fg = fg or PAGE_CONFIG["title_fg"]
        bg = bg or PAGE_CONFIG["title_bg"]
        pady = pady if pady is not None else PAGE_CONFIG["title_padding"]
        anchor = anchor or PAGE_CONFIG["title_anchor"]

        if self.title_label:
            self.title_label.config(text=text)
        else:
            self.title_label = self.ttk.Label(
                self,
                text=text,
                style=style,
                font=font,
                foreground=fg,
                background=bg
            )
            self.title_label.pack(pady=pady, anchor=anchor)

    def add_centered_frame(self, width=None, height=None):
        center_frame = Frame(self, bg=self["bg"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        if width: center_frame.configure(width=width)
        if height: center_frame.configure(height=height)
        return center_frame
