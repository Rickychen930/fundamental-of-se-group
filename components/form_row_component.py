# components/form_row_component.py
import tkinter as tk
from components.label_component import LabelComponent
from components.text_input_component import TextInputComponent
from components.button_component import ButtonComponent

class FormRowComponent:
    def __init__(self, master, label_text, input_var=None, button_text=None, button_action=None, show=None):
        self.frame = tk.Frame(master, bg=master["bg"])
        self.label = LabelComponent(
            self.frame,
            text=label_text,
            bg=master["bg"],
            layout="grid",
            padding=(6, 6)
        )
        self.label.render()
        self.label.get_widget().grid(row=0, column=0, sticky="e")

        self.input = TextInputComponent(
            self.frame,
            height=1,
            width=30,
            layout="grid",
            padding=(6, 6)
        )
        self.input.render()
        self.input_widget = self.input.get_widget()
        if show:
            self.input_widget.config(show=show)
        self.input_widget.grid(row=0, column=1, sticky="ew")

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
        return self.input

    def get_widget(self):
        return self.frame
