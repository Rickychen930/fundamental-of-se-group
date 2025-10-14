ACTIVE_LANGUAGE = "en"

STRINGS = {
    "en": {
        # App & Splash
        "app_title": "My Application",
        "loading_text": "Loading...",
        "welcome_message": "Welcome to My Application!",
        "exit_prompt": "Are you sure you want to exit?",

        # Login Page
        "login_title": "Login",
        "login_subtitle": "Login to your account",
        "login_button": "Login",
        "username_label": "Username",
        "password_label": "Password",
        "register_button": "Create Account",
        "cancel_button": "Cancel",
        "forgot_password": "Forgot Password?",
        "login_error": "Invalid username or password",

        # Register Page
        "register_title": "Register",
        "register_subtitle": "Create a new account to continue",
        "register_button": "Register",
        "email_label": "Email",
        "confirm_password_label": "Confirm Password",
        "back_to_login": "Back to Login",
        "registration_success": "Registration successful!",
        "registration_error": "Registration failed. Please try again.",

        # Alerts & Message Boxes
        "alert_info": "Information",
        "alert_warning": "Warning",
        "alert_error": "Error",
        "alert_success": "Success",
        "messagebox_ok": "OK",
        "messagebox_cancel": "Cancel",
        "messagebox_yes": "Yes",
        "messagebox_no": "No",

        # Navigation & General
        "home": "Home",
        "settings": "Settings",
        "profile": "Profile",
        "logout": "Logout",
        "language_label": "Language",
        "theme_label": "Theme",
        "save_button": "Save",
        "close_button": "Close"
    }
}

def get_text(key):
    return STRINGS.get(ACTIVE_LANGUAGE, {}).get(key, f"[{key}]")
