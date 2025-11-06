import tkinter as tk
from pl.pl_timer import GameTimer

class TimerAdapter:
    def __init__(self, root: tk.Tk, game_timer: GameTimer, update_interval: int = 1000):
        self.root = root
        self.game_timer = game_timer
        self.update_interval = update_interval
        self.time_var = tk.StringVar()
        self._after_id = None
        self._update_display()

    def _format(self, seconds: int) -> str:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

    def _tick(self):
        if self.game_timer.running:
            self.game_timer.tick(1)
            self._update_display()
            self._after_id = self.root.after(self.update_interval, self._tick)

    def _update_display(self):
        self.time_var.set(self._format(self.game_timer.elapsed()))

    def start(self):
        if not self.game_timer.running:
            self.game_timer.start()
        if self._after_id is None:
            self._tick()

    def stop(self):
        self.game_timer.stop()
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def destroy(self):
        self.stop()