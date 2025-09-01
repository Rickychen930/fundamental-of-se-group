ACTIVE_LANGUAGE = "en"

STRINGS = {
    "en": {
        "app_title": "Apps",
        "login_title": "Login",
        "login_button": "Submit",
        "username_label": "Username",
        "password_label": "Password",
        "loading_text": "Loading..."
    }
}

def get_text(key):
    return STRINGS.get(ACTIVE_LANGUAGE, {}).get(key, f"[{key}]")
