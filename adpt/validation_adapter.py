# adpt/validation_adapter.py
import tkinter as tk
from pl.pl_validator import valid_for  # uses board_getter callable

class ValidationAdapter:
    def __init__(self, core_game, ui_builder, initial_mode='v1'):
        self.core = core_game
        self.ui = ui_builder
        self.mode = initial_mode

    def set_mode(self, mode: str):
        self.mode = mode
        self.revalidate_all()

    def revalidate_all(self):
        for r in range(9):
            for c in range(9):
                val = self.ui.get_cell_value(r, c)
                text = '' if val == 0 else str(val)
                self.handle_input(r, c, text)

    def handle_input(self, row: int, col: int, text: str) -> bool:
        """
        Returns True if input is accepted (or allowed with coloring).
        Behavior mirrors previous v1 (highlight invalid) and v2 (reject invalid).
        """
        widget = self.ui.get_widget(row, col)
        # Empty input handling
        if text.strip() == "":
            self.core.set_cell(row, col, 0)
            self.ui.set_cell_visual(row, col, bg='white', fg='black')
            return True

        try:
            num = int(text)
            if not (1 <= num <= 9):
                raise ValueError()
        except ValueError:
            if self.mode == 'v2':
                # schedule clear after idle to avoid recursion
                if isinstance(widget, tk.Entry):
                    widget.after_idle(lambda: (widget.delete(0, tk.END)))
                self.ui.set_cell_visual(row, col, bg='white', fg='black')
                self.core.set_cell(row, col, 0)
                return False
            else:
                self.ui.set_cell_visual(row, col, bg='#ffcccc', fg='red')
                return True

        # Use pl.pl_validator.valid_for via a board getter that reads UI values
        board_getter = lambda r, c: self.ui.get_cell_value(r, c)
        valid = valid_for(board_getter, num, row, col)
        if valid:
            self.core.set_cell(row, col, num)
            self.ui.set_cell_visual(row, col, bg='white', fg='black')
            return True
        else:
            if self.mode == 'v2':
                if isinstance(widget, tk.Entry):
                    widget.after_idle(lambda: (widget.delete(0, tk.END)))
                self.ui.set_cell_visual(row, col, bg='white', fg='black')
                self.core.set_cell(row, col, 0)
                return False
            else:
                # v1: highlight then accept (so board state shows the value)
                self.ui.set_cell_visual(row, col, bg='#ffcccc', fg='red')
                self.core.set_cell(row, col, num)
                return True