from .component import Component
from resources.parameters.app_parameters import ALERT_CONFIG

class AlertComponent(Component):
    def __init__(
        self,
        master,
        message=None,
        style=None,
        layout=None,
        padding=None,
        visible=True,
        **kwargs
    ):
        super().__init__(
            master,
            style=style or ALERT_CONFIG["style"],
            layout=layout or ALERT_CONFIG["layout"],
            padding=padding or ALERT_CONFIG["padding"],
            **kwargs
        )
        self._message = message or ""
        self._visible = visible
        self.label = None

        self.create_component()

    def create_component(self):
        config = {
            "text": self._message,
            "style": self.get_style(),
            "wraplength": ALERT_CONFIG.get("wraplength", 400),
            "justify": ALERT_CONFIG.get("justify", "left")
        }
        config.update(self.get_extra())
        self.label = self.get_ttk().Label(self.get_root(), **config)

    def render(self):
        if not self._visible:
            return

        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self.label.pack(padx=padx, pady=pady, anchor="w")
        elif layout == "grid":
            self.label.grid(padx=padx, pady=pady, sticky="w")
        elif layout == "place":
            self.label.place(relx=0.5, rely=0.5, anchor="center")

    def set_message(self, message):
        self._message = message
        if self.label:
            self.label.config(text=message)

    def hide(self):
        self._visible = False
        if self.label:
            self.label.pack_forget()

    def show(self):
        self._visible = True
        self.render()
