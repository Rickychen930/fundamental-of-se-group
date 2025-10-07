from .component import Component
from .label_component import LabelComponent
from .text_input_component import TextInputComponent
from resources.parameters.app_parameters import FORM_FIELD_CONFIG

class FormField(Component):
    def __init__(
        self,
        master,
        label_text,
        label_style=None,
        label_font=None,
        label_fg=None,
        label_bg=None,
        input_height=None,
        input_width=None,
        input_font=None,
        input_fg=None,
        input_bg=None,
        input_bd=None,
        input_relief=None,
        layout=None,
        padding=None,
        autoselect=None,
        **kwargs
    ):
        super().__init__(
            master,
            layout=layout or FORM_FIELD_CONFIG["layout"],
            padding=padding or FORM_FIELD_CONFIG["padding"],
            **kwargs
        )
        self._label_text = label_text
        self._label_style = label_style or FORM_FIELD_CONFIG["label_style"]
        self._label_font = label_font or FORM_FIELD_CONFIG["label_font"]
        self._label_fg = label_fg or FORM_FIELD_CONFIG["label_fg"]
        self._label_bg = label_bg or FORM_FIELD_CONFIG["label_bg"]

        self._input_height = input_height if input_height is not None else FORM_FIELD_CONFIG["input_height"]
        self._input_width = input_width if input_width is not None else FORM_FIELD_CONFIG["input_width"]
        self._input_font = input_font or FORM_FIELD_CONFIG["input_font"]
        self._input_fg = input_fg or FORM_FIELD_CONFIG["input_fg"]
        self._input_bg = input_bg or FORM_FIELD_CONFIG["input_bg"]
        self._input_bd = input_bd if input_bd is not None else FORM_FIELD_CONFIG["input_bd"]
        self._input_relief = input_relief or FORM_FIELD_CONFIG["input_relief"]
        self._autoselect = autoselect if autoselect is not None else FORM_FIELD_CONFIG["autoselect"]

        self.label = None
        self.text_input = None

        self.create_component()

    def create_component(self):
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
            height=self._input_height,
            width=self._input_width,
            font=self._input_font,
            fg=self._input_fg,
            bg=self._input_bg,
            bd=self._input_bd,
            relief=self._input_relief,
            layout=self.get_layout(),
            padding=self.get_padding(),
            autoselect=self._autoselect
        )

        self.label_widget = self.label.get_widget()
        self.input_widget = self.text_input.get_widget()

    def render(self):
        self.label.render()
        self.text_input.render()

    def get_value(self):
        return self.text_input.get_text()

    def set_value(self, value):
        self.text_input.set_text(value)
