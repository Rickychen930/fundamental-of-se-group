import tkinter as tk
from components.label_component import LabelComponent
from components.text_input_component import TextInputComponent
from components.button_component import ButtonComponent

class FormRowComponent:
    """
    FormRowComponent creates a single row in a form layout, consisting of:
    - A label on the left
    - A text input field in the center
    - An optional button on the right

    This component is useful for login forms, search bars, or any structured input row.
    """

    def __init__(
        self,
        master,
        label_text,
        input_var=None,
        button_text=None,
        button_action=None,
        show=None
    ):
        """
        Initialize the form row with label, input, and optional button.

        Args:
            master (tk.Widget): Parent container.
            label_text (str): Text to display in the label.
            input_var (tk.StringVar, optional): Variable to bind to the input field.
            button_text (str, optional): Text to display on the button.
            button_action (callable, optional): Function to call when the button is clicked.
            show (str, optional): Character to mask input (e.g., '*' for passwords).
        """
        self.frame = tk.Frame(master, bg=master["bg"])

        # Label component
        self.label = LabelComponent(
            self.frame,
            text=label_text,
            bg=master["bg"],
            layout="grid",
            padding=(6, 6)
        )
        self.label.render()
        self.label.get_widget().grid(row=0, column=0, sticky="e")

        # Text input component
        self.input = TextInputComponent(
            self.frame,
            textvariable=input_var,
            width=30,
            layout="grid",
            padding=(6, 6),
            show=show
        )
        self.input.render()
        self.input_widget = self.input.get_widget()
        self.input_widget.grid(row=0, column=1, sticky="ew")

        # Optional button component
        self.button = None
        if button_text and button_action:
            self.button = ButtonComponent(
                self.frame,
                name=button_text,
                action=button_action,
                layout="grid",
                padding=(6, 6)
            )
            self.button.create_component()
            self.button.button_widget.grid(row=0, column=2, padx=6, pady=6)

    def get_input(self):
        """
        Get the TextInputComponent instance.

        Returns:
            TextInputComponent: The input component for value access or manipulation.
        """
        return self.input

    def get_widget(self):
        """
        Get the root frame containing the form row.

        Returns:
            tk.Frame: The container frame for layout placement.
        """
        return self.frame
