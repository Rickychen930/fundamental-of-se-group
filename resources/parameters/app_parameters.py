from resources.colors.colors import get_color
from resources.strings.strings import get_text

# COMPONENT DEFAULTS
COMPONENT_DEFAULTS = {
    "background": get_color("background"),
    "foreground": get_color("text_primary"),
    "font": ("Segoe UI", 11),
    "layout": "pack",
    "padding": (0, 0),
    "style": None
}

BUTTON_CONFIG = {
    "style": "Primary.TButton",
    "font": ("Segoe UI", 11, "bold"),
    "fg": get_color("text_on_accent"),
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
    "layout": "pack",  # can be overridden with "grid"
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

# PAGE CONFIGS

APP_CONFIG = {
    "title": get_text("app_title"),
    "background_color": get_color("background")
    # Geometry is omitted to allow auto-sizing
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

PAGE_CONFIG = {
    "default_bg": get_color("background"),
    "title_style": "Title.TLabel",
    "title_font": ("Segoe UI", 20, "bold"),
    "title_fg": get_color("title_fg"),
    "title_bg": get_color("title_bg"),
    "title_padding": 30,
    "title_anchor": "center"
}

LOGIN_CONFIG = {
    "background_color": get_color("surface"),
    "title_text": get_text("login_title"),
    "title_font": ("Segoe UI", 20, "bold"),
    "title_padding": 24,
    "subtitle_text": get_text("login_subtitle"),
    "subtitle_font": ("Segoe UI", 12),
    "subtitle_fg": get_color("text_secondary"),
    "form_padding_y": 12,
    "form_padding_x": 24,
    "field_label_style": "FieldLabel.TLabel",
    "field_label_font": ("Segoe UI", 12),
    "username_label": get_text("username_label"),
    "password_label": get_text("password_label"),
    "input_width": 40,
    "input_font": ("Segoe UI", 11),
    "input_fg": get_color("text_primary"),
    "input_bg": get_color("surface"),
    "input_padding": (5, 10),
    "button_text": get_text("login_button"),
    "button_style": "Primary.TButton",
    "button_font": ("Segoe UI", 11, "bold"),
    "button_fg": get_color("text_on_accent"),
    "button_bg": get_color("accent"),
    "button_padding": (30, 10),
    "button_layout": "pack",
    "button_frame_padding": 20,
    "register_button_text": get_text("register_button"),
    "register_button_style": "Secondary.TButton",
    "register_button_layout": "pack",
    "register_button_padding": (20, 10),
    "title_fg": get_color("title_fg"),
    "title_bg": get_color("title_bg"),
    "cancel_text":get_text("cancel_button")

}

REGISTER_CONFIG = {
    "background_color": get_color("surface"),
    "title_text": get_text("register_title"),
    "title_font": ("Segoe UI", 20, "bold"),
    "title_padding": 24,
    "subtitle_text": get_text("register_subtitle"),
    "subtitle_font": ("Segoe UI", 12),
    "subtitle_fg": get_color("text_secondary"),
    "form_padding_y": 12,
    "form_padding_x": 24,
    "field_label_style": "FieldLabel.TLabel",
    "field_label_font": ("Segoe UI", 12),
    "username_label": get_text("username_label"),
    "email_label": get_text("email_label"),
    "password_label": get_text("password_label"),
    "confirm_password_label": get_text("confirm_password_label"),
    "input_width": 40,
    "input_font": ("Segoe UI", 11),
    "input_fg": get_color("text_primary"),
    "input_bg": get_color("surface"),
    "input_padding": (5, 10),
    "button_text": get_text("register_button"),
    "button_style": "Primary.TButton",
    "button_font": ("Segoe UI", 11, "bold"),
    "button_fg": get_color("text_on_accent"),
    "button_bg": get_color("accent"),
    "button_padding": (30, 10),
    "button_layout": "pack",
    "button_frame_padding": 20,
    "back_button_text": get_text("back_to_login"),
    "back_button_style": "Secondary.TButton",
    "back_button_layout": "pack",
    "back_button_padding": (20, 10)
}

ALERT_CONFIG = {
    "style": "Alert.TLabel",
    "layout": "pack",
    "padding": (10, 5),
    "wraplength": 400,
    "justify": "left"
}

MESSAGEBOX_CONFIG = {
    "style": "MessageBox.TFrame",
    "layout": "pack",
    "padding": (10, 10),
    "wraplength": 400,
    "justify": "left",
    "default_title": "Notice",
    "title_style": "MessageBoxTitle.TLabel",
    "message_style": "MessageBoxText.TLabel"
}

# Subject catalog 
SUBJECT_CATALOG = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "English",
    "Programming",
]

