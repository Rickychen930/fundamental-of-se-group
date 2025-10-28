import sys

# ---------- CLI launcher ----------
def run_cli():
    """
    Launch the Command Line Interface (CLI) version of the application.
    """
    from view.CLI.app import App  # Imported here to avoid unnecessary dependencies if GUI mode is used.
    root = App()
    root.run()


# ---------- GUI launcher ----------
def run_gui():
    """
    Launch the Graphical User Interface (GUI) version of the application.
    """
    from view.GUI.app import App  # Imported here to avoid loading GUI modules unless needed.
    root = App()
    root.run()


# ---------- Main entry point ----------
def main():
    """
    Prompt the user to choose between CLI or GUI mode, then start the appropriate interface.
    """
    print("Choose mode to run:")
    print("1. CLI")
    print("2. GUI")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        run_cli()
    elif choice == "2":
        run_gui()
    else:
        # Exit gracefully if invalid input
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)


# ---------- Program start ----------
if __name__ == "__main__":
    main()
