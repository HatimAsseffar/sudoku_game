import tkinter as tk

class ValidationController:
    def __init__(self, parent, initial_mode, game=None):
        self.game = game
        self.v1_var = tk.BooleanVar(value=(initial_mode == 'v1'))
        self.v2_var = tk.BooleanVar(value=(initial_mode == 'v2'))

        self.v1_check = tk.Checkbutton(
            parent,
            text="Highlight wrong Input",
            variable=self.v1_var,
            command=lambda: self.toggle_mode('v1')
        )
        self.v1_check.pack(side=tk.LEFT, padx=5)

        self.v2_check = tk.Checkbutton(
            parent,
            text="Auto-Correct",
            variable=self.v2_var,
            command=lambda: self.toggle_mode('v2')
        )
        self.v2_check.pack(side=tk.LEFT, padx=5)

        self.toggle_mode(initial_mode)

    def toggle_mode(self, mode):
        self.v1_var.set(False)
        self.v2_var.set(False)
        if mode == 'v1':
            self.v1_var.set(True)
        else:
            self.v2_var.set(True)

        if self.game and hasattr(self.game, 'validation_adapter'):
            self.game.validation_adapter.set_mode(mode)
                                  
            self.game.validation_adapter.revalidate_all()