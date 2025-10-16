import sys

def run_cli():
    from view.CLI.app import App
    root = App()
    root.run()

def run_gui():
    from view.GUI.app import App
    root = App()
    root.run()

def main():
    print("Choose mode to run:")
    print("1. CLI")
    print("2. GUI")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        run_cli()
    elif choice == "2":
        run_gui()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)

if __name__ == "__main__":
    main()
