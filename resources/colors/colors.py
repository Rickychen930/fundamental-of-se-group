COLOR_PALETTE = {
    "light": {
        "background": "#f5f7fa",
        "surface": "#ffffff",
        "text_primary": "#000000",
        "text_secondary": "#333333",
        "accent": "#007acc",
        "accent_hover": "#005f99",
        "border": "#e0e0e0",
        "title_bg": "#34495e",
        "title_fg": "#ffffff"
    },
    "dark": {
        "background": "#1e1e1e",
        "surface": "#2c2c2c",
        "text_primary": "#f0f0f0",
        "text_secondary": "#cccccc",
        "accent": "#00aaff",
        "accent_hover": "#0088cc",
        "border": "#444444",
        "title_bg": "#222831",
        "title_fg": "#eeeeee"
    }
}

# Mode
ACTIVE_THEME = "light"

def get_color(key):
    return COLOR_PALETTE[ACTIVE_THEME].get(key)
