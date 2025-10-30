from tkinter import Frame, BOTH
from tkinter import ttk
from resources.parameters.app_parameters import PAGE_CONFIG

class BasePage(Frame):
    """
    BasePage provides a styled container with flexible layout options.
    It supports background configuration, title rendering, and centered content.
    """

    def __init__(self, master, bg=None, layout="pack", **kwargs):
        """
        Initialize the base page with layout and background.

        Args:
            master (tk.Tk or tk.Frame): Parent widget.
            bg (str): Background color.
            layout (str): Layout type: 'pack', 'grid', or 'place'.
            **kwargs: Additional Frame options.
        """
        bg = bg or PAGE_CONFIG.get("default_bg", "#FFFFFF")
        super().__init__(master, bg=bg, **kwargs)

        self.master = master
        self._layout = layout
        self.title_label = None

        self._apply_layout()

    def _apply_layout(self):
        """Apply layout manager based on configuration."""
        if self._layout == "pack":
            self.pack(fill=BOTH, expand=True)
        elif self._layout == "grid":
            self.grid(sticky="nsew")
        elif self._layout == "place":
            self.place(relx=0.5, rely=0.5, anchor="center")

    def clear_page(self):
        """Remove all child widgets except the title label."""
        for widget in self.winfo_children():
            if widget != self.title_label:
                widget.destroy()

    def set_background_color(self, color=None):
        """Set the background color of the page."""
        self.configure(bg=color or PAGE_CONFIG.get("default_bg", "#FFFFFF"))

    def set_title(self, text, style=None, font=None, fg=None, bg=None, pady=None, anchor=None):
        """
        Set or update the page title label.

        Args:
            text (str): Title text.
            style (str): ttk style name.
            font (tuple): Font tuple.
            fg (str): Foreground color.
            bg (str): Background color.
            pady (int): Vertical padding.
            anchor (str): Anchor position for pack layout.
        """
        style = style or PAGE_CONFIG.get("title_style", "Title.TLabel")
        font = font or PAGE_CONFIG.get("title_font", ("Helvetica", 16, "bold"))
        fg = fg or PAGE_CONFIG.get("title_fg", "#000000")
        bg = bg or PAGE_CONFIG.get("title_bg", self["bg"])
        pady = pady if pady is not None else PAGE_CONFIG.get("title_padding", 10)
        anchor = anchor or PAGE_CONFIG.get("title_anchor", "center")

        if self.title_label:
            self.title_label.config(text=text)
        else:
            self.title_label = ttk.Label(
                self,
                text=text,
                style=style,
                font=font,
                foreground=fg,
                background=bg
            )
            self.title_label.pack(pady=pady, anchor=anchor)

    def add_centered_frame(self, width=None, height=None):
        """
        Add a centered frame inside the page.

        Args:
            width (int): Optional width of the frame.
            height (int): Optional height of the frame.

        Returns:
            Frame: The centered frame instance.
        """
        center_frame = Frame(self, bg=self["bg"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        if width:
            center_frame.configure(width=width)
        if height:
            center_frame.configure(height=height)

        return center_frame
