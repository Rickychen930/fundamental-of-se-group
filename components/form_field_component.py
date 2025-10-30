from .component import Component
from .label_component import LabelComponent
from .text_input_component import TextInputComponent
from resources.parameters.app_parameters import FORM_FIELD_CONFIG

class FormField(Component):
    """
    FormField combines a label and a text input into a unified layout.
    Useful for structured form inputs such as login, registration, or data entry.
    """

    def __init__(
        self,
        master,
        label_text,
        label_style=None,
        label_font=None,
        label_fg=None,
        label_bg=None,
        input_width=None,
        input_font=None,
        input_fg=None,
        input_bg=None,
        input_bd=None,
        input_relief=None,
        layout=None,
        padding=None,
        autoselect=None,
        show=None,
        **kwargs
    ):
        """
        Initialize the form field component.

        Args:
            master (tk.Widget): Parent widget.
            label_text (str): Text for the label.
            label_style (str): ttk style name for the label.
            label_font (tuple): Font tuple for the label.
            label_fg (str): Foreground color for the label.
            label_bg (str): Background color for the label.
            input_width (int): Width of the input field.
            input_font (tuple): Font tuple for the input.
            input_fg (str): Foreground color for the input.
            input_bg (str): Background color for the input.
            input_bd (int): Border width for the input.
            input_relief (str): Relief style for the input.
            layout (str): Layout manager ('pack', 'grid', 'place').
            padding (tuple): (padx, pady) values.
            autoselect (bool): Whether to auto-select text on focus.
            show (str): Mask character for password fields.
            **kwargs: Additional configuration passed to base Component.
        """
        super().__init__(
            master,
            layout=layout or FORM_FIELD_CONFIG["layout"],
            padding=padding or FORM_FIELD_CONFIG["padding"],
            **kwargs
        )

        # Label configuration
        self._label_text = label_text
        self._label_style = label_style or FORM_FIELD_CONFIG["label_style"]
        self._label_font = label_font or FORM_FIELD_CONFIG["label_font"]
        self._label_fg = label_fg or FORM_FIELD_CONFIG["label_fg"]
        self._label_bg = label_bg or FORM_FIELD_CONFIG["label_bg"]

        # Input configuration
        self._input_width = input_width or FORM_FIELD_CONFIG["input_width"]
        self._input_font = input_font or FORM_FIELD_CONFIG["input_font"]
        self._input_fg = input_fg or FORM_FIELD_CONFIG["input_fg"]
        self._input_bg = input_bg or FORM_FIELD_CONFIG["input_bg"]
        self._input_bd = input_bd if input_bd is not None else FORM_FIELD_CONFIG["input_bd"]
        self._input_relief = input_relief or FORM_FIELD_CONFIG["input_relief"]
        self._autoselect = autoselect if autoselect is not None else FORM_FIELD_CONFIG["autoselect"]
        self._show = show

        self.label = None
        self.text_input = None
        self.label_widget = None
        self.input_widget = None

        self.create_component()

    def create_component(self):
        """Create and configure the label and input components."""
        self.label = LabelComponent(
            self.get_root(),
            text=self._label_text,
            style=self._label_style,
            font=self._label_font,
            fg=self._label_fg,
            bg=self._label_bg,
            layout=self.get_layout(),
            padding=self.get_padding()
        )

        self.text_input = TextInputComponent(
            self.get_root(),
            width=self._input_width,
            font=self._input_font,
            fg=self._input_fg,
            bg=self._input_bg,
            bd=self._input_bd,
            relief=self._input_relief,
            layout=self.get_layout(),
            padding=self.get_padding(),
            autoselect=self._autoselect,
            show=self._show
        )

        self.label_widget = self.label.get_widget()
        self.input_widget = self.text_input.get_widget()

    def render(self):
        """Render both label and input components."""
        self.label.render()
        self.text_input.render()

    def get_value(self):
        """
        Get the current value of the input field.

        Returns:
            str: Text entered in the input field.
        """
        return self.text_input.get_text()

    def set_value(self, value):
        """
        Set the value of the input field.

        Args:
            value (str): Text to populate in the input field.
        """
        self.text_input.set_text(value)
