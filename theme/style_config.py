from tkinter import ttk
from resources.colors.colors import get_color

def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")

    # Title Label
    style.configure("Title.TLabel",
        font=("Segoe UI", 20, "bold"),
        foreground=get_color("title_fg"),
        background=get_color("title_bg"),
        padding=10
    )

    # Splash Screen Label
    style.configure("SplashLabel.TLabel",
        font=("Segoe UI", 16, "bold"),
        foreground=get_color("text_secondary"),
        background=get_color("surface"),
        padding=10
    )

    # Field Label (Username, Password)
    style.configure("FieldLabel.TLabel",
        font=("Segoe UI", 12),
        foreground=get_color("text_secondary"),
        background=get_color("background"),
        padding=5
    )

    # Primary Button
    style.configure("Primary.TButton",
        font=("Segoe UI", 11, "bold"),
        foreground=get_color("text_primary"),
        background=get_color("accent"),
        padding=6
    )

    style.map("Primary.TButton",
        background=[("active", get_color("accent_hover"))]
    )

    # Progress Bar
    style.configure("TProgressbar",
        troughcolor=get_color("border"),
        background=get_color("accent"),
        bordercolor=get_color("surface")
    )
