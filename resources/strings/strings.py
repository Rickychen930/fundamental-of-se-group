ACTIVE_LANGUAGE = "en"

STRINGS = {
    "en": {
        # App & Splash
        "app_title": "My Application",
        "loading_text": "Loading...",

        # Login Page
        "login_title": "Login",
        "login_subtitle": "Login",
        "login_button": "Login",
        "username_label": "Username",
        "password_label": "Password",
        "register_button": "Create Account",
        "cancel_button": "Cancel",

        # Register Page
        "register_title": "Register",
        "register_subtitle": "Create a new account to continue",
        "register_button": "Register",
        "email_label": "Email",
        "confirm_password_label": "Confirm Password",
        "back_to_login": "Back to Login"
    }
}

def get_text(key):
    return STRINGS.get(ACTIVE_LANGUAGE, {}).get(key, f"[{key}]")
