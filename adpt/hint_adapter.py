import tkinter as tk
from typing import Optional

class HintAdapter:
    def __init__(self, core_game, ui_builder):
        self.core = core_game
        self.ui = ui_builder
        self.button: Optional[tk.Button] = None
        if hasattr(self.core, 'register_on_cell_changed'):
            self.core.register_on_cell_changed(self._on_core_change)

    def set_button(self, btn: tk.Button):
        self.button = btn
        self._update_button()
        self.button.config(command=self.on_request_hint)

    def _update_button(self):
        if not self.button:
            return
        hints = getattr(self.core, 'hints_remaining', 0)
        text = f"Hint ({hints})"
        state = 'normal' if hints > 0 else 'disabled'
        self.button.config(text=text, state=state)

    def on_request_hint(self):
        if not hasattr(self.core, 'request_hint'):
            empties = getattr(self.core, 'empty_cells', lambda: [])()
            if not empties:
                return False
            r, c = empties[0]
            val = getattr(self.core, 'solution', [[0]*9])[r][c]
            self.core.set_cell(r, c, val)
            self.ui.set_cell_value(r, c, val)
            return True

        hint = self.core.request_hint()
        if hint:
            r, c, v = hint
            self.ui.set_cell_value(r, c, v)
        self._update_button()
        return True

    def _on_core_change(self, r, c, v):
        self.ui.set_cell_value(r, c, v)
        self._update_button()