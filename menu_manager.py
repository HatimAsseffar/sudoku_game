                 
import tkinter as tk
from tkinter import messagebox
from menus_saves import MainMenu, SaveSelectionWindow, DifficultySelector
from validation import ValidationController

class MenuManager:
    def __init__(self, game, root, styles):
        self.game = game
        self.root = root
        self.styles = styles

    def show_main_menu(self):
        MainMenu(
            root=self.root,
            frame_bg=self.styles['frame_bg'],
            button_style=self.styles['button_style'],
            autosave_manager=self.game.autosave_adapter,
            start_callback=self.on_start_new_game,
            continue_callback=self.on_continue_game
        )

    def on_start_new_game(self):
        self.game.show_difficulty_selector()

    def on_continue_game(self):
        saved_data = self.game.autosave_adapter.load()
        if not saved_data:
            tk.messagebox.showinfo("No Save Found", "No saved game available!")
            return
        SaveSelectionWindow(
            root=self.root,
            saved_data=saved_data,
            styles=self.game.styles,
            ui_builder=self.game.ui_builder,
            start_game=self.game.start_game
        )

    def show_difficulty_selector(self):
        DifficultySelector(
            root=self.root,
            difficulties=self.game.DIFFICULTIES,
            frame_bg=self.styles['frame_bg'],
            button_style=self.styles['button_style'],
            callback=self.on_difficulty_selected
        )

    def on_difficulty_selected(self, difficulty):
        self.game.start_game(difficulty)

    def show_settings_window(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Validation Settings")
        settings_window.geometry("300x100")

        controller_frame = tk.Frame(settings_window)
        controller_frame.pack(pady=10)
        current_mode = getattr(self.game, 'validation_adapter', None)
        mode = current_mode.mode if current_mode else 'v1'
        ValidationController(controller_frame, mode, game=self.game)