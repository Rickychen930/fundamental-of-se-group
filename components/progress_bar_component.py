from .component import Component
from resources.parameters.app_parameters import PROGRESS_CONFIG

class ProgressBarComponent(Component):
    """
    ProgressBarComponent wraps a ttk.Progressbar with layout, animation, and value control.
    Supports determinate and indeterminate modes with optional autostart animation.
    """

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
        """
        Initialize the progress bar component.

        Args:
            master (tk.Widget): Parent widget.
            value (int, optional): Initial progress value (0–100).
            interval (int, optional): Milliseconds between animation steps.
            step (int, optional): Increment per animation step.
            style (str, optional): ttk style name.
            length (int, optional): Length of the progress bar in pixels.
            mode (str, optional): 'determinate' or 'indeterminate'.
            orient (str, optional): 'horizontal' or 'vertical'.
            layout (str, optional): Layout manager ('pack', 'grid', 'place').
            padding (tuple, optional): (padx, pady) values.
            autostart (bool, optional): Whether to start animation automatically.
            **kwargs: Additional configuration passed to base Component.
        """
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
        self._mode = mode or PROGRESS_CONFIG["mode"]
        self._orient = orient or PROGRESS_CONFIG["orient"]
        self._autostart = autostart if autostart is not None else PROGRESS_CONFIG["autostart"]

        self.progress = None
        self.create_component()

    def create_component(self):
        """Create the internal ttk.Progressbar widget with configuration."""
        config = {
            "orient": self._orient,
            "length": self._length,
            "mode": self._mode,
            "style": self.get_style()
        }
        config.update(self.get_extra())
        self.progress = self.get_ttk().Progressbar(self.get_root(), **config)

    def render(self):
        """Render the progress bar using the specified layout manager."""
        layout = self.get_layout()
        padx, pady = self.get_padding()

        if layout == "pack":
            self.progress.pack(padx=padx, pady=pady)
        elif layout == "grid":
            self.progress.grid(padx=padx, pady=pady)
        elif layout == "place":
            self.progress.place(relx=0.5, rely=0.5, anchor="center")

        if self._autostart:
            self.start_loading()

    def start_loading(self):
        """
        Begin animating the progress bar.
        For 'determinate' mode, it increments until 100.
        For 'indeterminate' mode, it loops indefinitely.
        """
        if self._mode == "indeterminate":
            self.progress.start(self._interval)
        else:
            self._update()

    def _update(self):
        """Internal method to increment progress in determinate mode."""
        if self._value < 100:
            self._value += self._step
            self.progress["value"] = self._value
            self.get_root().after(self._interval, self._update)

    def reset(self):
        """Reset the progress bar to 0 and stop animation if running."""
        self._value = 0
        self.progress["value"] = 0
        if self._mode == "indeterminate":
            self.progress.stop()

    def set_value(self, value):
        """
        Set the progress bar to a specific value.

        Args:
            value (int): Value between 0 and 100.
        """
        self._value = value
        self.progress["value"] = value
