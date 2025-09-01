from .component import Component
from resources.parameters.app_parameters import PROGRESS_CONFIG

class ProgressBarComponent(Component):
    def __init__(
        self,
        master,
        value=None,
        interval=None,
        step=None,
        style=None,
        length=None,
        mode=None,
        orient=None,
        layout=None,
        padding=None,
        autostart=None,
        **kwargs
    ):
        super().__init__(
            master,
            style=style or PROGRESS_CONFIG["style"],
            layout=layout or PROGRESS_CONFIG["layout"],
            padding=padding or PROGRESS_CONFIG["padding"],
            **kwargs
        )
        self._value = value if value is not None else PROGRESS_CONFIG["value"]
        self._interval = interval if interval is not None else PROGRESS_CONFIG["interval"]
        self._step = step if step is not None else PROGRESS_CONFIG["step"]
        self._length = length if length is not None else PROGRESS_CONFIG["length"]
        self._mode = mode if mode is not None else PROGRESS_CONFIG["mode"]
        self._orient = orient if orient is not None else PROGRESS_CONFIG["orient"]
        self._autostart = autostart if autostart is not None else PROGRESS_CONFIG["autostart"]
        self.progress = None

        self.create_component()

    def create_component(self):
        config = {
            "orient": self._orient,
            "length": self._length,
            "mode": self._mode,
            "style": self.get_style()
        }
        config.update(self.get_extra())
        self.progress = self.get_ttk().Progressbar(self.get_root(), **config)

    def render(self):
        layout = self.get_layout()
        pad = self.get_padding()

        if layout == "pack":
            self.progress.pack(pady=pad[0] if pad else 10)
        elif layout == "grid":
            self.progress.grid(pady=pad[0] if pad else 10)
        elif layout == "place":
            self.progress.place(relx=0.5, rely=0.5, anchor="center")

        if self._autostart:
            self.start_loading()

    def start_loading(self):
        self._update()

    def _update(self):
        if self._value < 100:
            self._value += self._step
            self.progress["value"] = self._value
            self.get_root().after(self._interval, self._update)

    def reset(self):
        self._value = 0
        self.progress["value"] = 0

    def set_value(self, value):
        self._value = value
        self.progress["value"] = value
