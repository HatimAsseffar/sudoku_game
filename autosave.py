import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class AutosaveManager:
    SAVE_FILE = "sudoku_autosave.json"

    def __init__(self, game):
        self.game = game

    def save_game(self):
        # Changed check from self.game.cells to self.game.ui_builder.cells
        if not hasattr(self.game.ui_builder, 'cells') or not self.game.current_difficulty:
            return

        save_data = {
            'puzzle': self.get_current_puzzle_state(),
            'hints_remaining': self.game.hint_manager.hints_remaining,  # Updated reference
            'timer': getattr(self.game.timer, 'elapsed_time', 0),
            'difficulty': self.game.current_difficulty,
            'validation_mode': self.game.validation.mode,  # Updated reference
            'timestamp': datetime.now().isoformat(),
            'solution': self.game.generator.solution,
            'cell_types': self.get_cell_types()
        }

        try:
            with open(self.SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)
        except IOError as e:
            print(f"Failed to save game: {e}")

    def load_game(self):
        try:
            with open(self.SAVE_FILE, 'r') as f:
                data = json.load(f)
                # Convert puzzle cells to integers
                if 'puzzle' in data:
                    converted_puzzle = []
                    for row in data['puzzle']:
                        converted_row = []
                        for cell in row:
                            stripped = str(cell).strip()
                            converted_cell = 0 if stripped in ('0', '') else int(stripped)
                            converted_row.append(converted_cell)
                        converted_puzzle.append(converted_row)
                    data['puzzle'] = converted_puzzle
                # Handle legacy saves without cell_types
                if 'cell_types' not in data:
                    cell_types = []
                    for row in data['puzzle']:
                        ct_row = []
                        for cell in row:
                            ct_row.append('text' if cell == 0 else 'label')
                        cell_types.append(ct_row)
                    data['cell_types'] = cell_types
                return data
        except (FileNotFoundError, json.JSONDecodeError, ValueError, KeyError):
            return None

    def clear_save(self):
        try:
            os.remove(self.SAVE_FILE)
        except FileNotFoundError:
            pass

    def get_current_puzzle_state(self):
        state = []
        # Access through UI Builder instead of game.cells
        for row in range(9):
            current_row = []
            for col in range(9):
                widget = self.game.ui_builder.cells[row][col]  # Updated
                if isinstance(widget, tk.Entry):
                    value = widget.get().strip()
                    num = int(value) if value else 0
                    current_row.append(num)
                else:
                    text = widget.cget('text')
                    num = int(text) if text else 0
                    current_row.append(num)
            state.append(current_row)
        return state

    def get_cell_types(self):
        cell_types = []
        # Access through UI Builder
        for row in range(9):
            current_row = []
            for col in range(9):
                widget = self.game.ui_builder.cells[row][col]  # Updated
                current_row.append('text' if isinstance(widget, tk.Entry) else 'label')
            cell_types.append(current_row)
        return cell_types

    #---------- Time Management & Autosave ----------#
    def prompt_save_on_exit(self):
        """Prompt user to save current game before closing."""
        response = messagebox.askyesno(
            "Save Progress",
            "Would you like to save your current game before exiting?",
            icon='question'
        )
        if response:
            self.save_game()
        # Close the game window afterwards
        if hasattr(self.game, 'on_close'):
            self.game.on_close()
