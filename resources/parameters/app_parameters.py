from resources.colors.colors import get_color
from resources.strings.strings import get_text
#COMPONENT

COMPONENT_DEFAULTS = {
    "background": get_color("background"),
    "font": ("Segoe UI", 11),
    "foreground": get_color("text_primary"),
    "layout": "pack",
    "padding": (0, 0),
    "style": None
}

BUTTON_CONFIG = {
    "style": "Primary.TButton",
    "font": ("Segoe UI", 11, "bold"),
    "fg": get_color("text_primary"),
    "bg": get_color("accent"),
    "padding": (20, 8),
    "layout": "pack"
}

TEXT_INPUT_CONFIG = {
    "height": 1,
    "width": 40,
    "font": ("Segoe UI", 11),
    "fg": get_color("text_primary"),
    "bg": get_color("surface"),
    "bd": 1,
    "relief": "solid",
    "layout": "pack",
    "padding": (5, 10),
    "autoselect": False
}

PROGRESS_CONFIG = {
    "value": 0,
    "interval": 30,
    "step": 2,
    "style": "TProgressbar",
    "length": 200,
    "mode": "determinate",
    "orient": "horizontal",
    "layout": "pack",
    "padding": (10,),
    "autostart": True
}

LABEL_CONFIG = {
    "style": "Default.TLabel",
    "font": ("Segoe UI", 12),
    "fg": get_color("text_secondary"),
    "bg": get_color("background"),
    "layout": "pack",
    "padding": (5, 0)
}

FORM_FIELD_CONFIG = {
    "label_style": "FieldLabel.TLabel",
    "label_font": ("Segoe UI", 12),
    "label_fg": get_color("text_secondary"),
    "label_bg": get_color("background"),

    "input_height": 1,
    "input_width": 40,
    "input_font": ("Segoe UI", 11),
    "input_fg": get_color("text_primary"),
    "input_bg": get_color("surface"),
    "input_bd": 1,
    "input_relief": "solid",

    "layout": "pack",
    "padding": (5, 10),
    "autoselect": False
}

#PAGE

APP_CONFIG = {
    "title": get_text("app_title"),
    "geometry": "1000x1000",
    "background_color": get_color("background")
}

SPLASH_CONFIG = {
    "background_color": get_color("surface"),
    "label_text": get_text("loading_text"),
    "label_style": "SplashLabel.TLabel",
    "label_padding": (0, 10),
    "progress_length": 250,
    "progress_step": 3,
    "progress_interval": 20,
    "progress_autostart": True,
    "progress_layout": "pack",
    "progress_padding": (0,)
}

LOGIN_CONFIG = {
    "background_color": get_color("surface"),
    "title_text": get_text("login_title"),
    "title_font": ("Segoe UI", 18, "bold"),
    "title_padding": 30,

    "form_padding_y": 10,
    "form_padding_x": 30,

    "field_label_style": "FieldLabel.TLabel",
    "field_label_font": ("Segoe UI", 12),
    "username_label": get_text("username_label"),
    "password_label": get_text("password_label"),
    "input_width": 40,
    "input_font": ("Segoe UI", 11),
    "input_fg": get_color("text_secondary"),
    "input_bg": get_color("surface"),
    "input_padding": (5, 10),

    "button_text": get_text("login_button"),
    "button_style": "Primary.TButton",
    "button_font": ("Segoe UI", 11, "bold"),
    "button_fg": get_color("text_primary"),
    "button_bg": get_color("accent"),
    "button_padding": (30, 10),
    "button_layout": "pack",
    "button_frame_padding": 20
}

PAGE_CONFIG = {
    "default_bg": get_color("background"),
    "title_style": "Title.TLabel",
    "title_font": ("Segoe UI", 20, "bold"),
    "title_fg": get_color("title_fg"),
    "title_bg": get_color("title_bg"),
    "title_padding": 30,
    "title_anchor": "center"
}


