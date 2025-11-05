import tkinter as tk

class SaveSelectionWindow:
    def __init__(self, root, saved_data, styles, ui_builder, start_game):
        self.window = tk.Toplevel(root)
        self.window.title("Continue Saved Game")
        self.window.configure(bg=styles['frame_bg'])
        self.window.geometry("250x150")
        self.saved_data = saved_data
        self.styles = styles
        self.setup_ui(root, ui_builder, saved_data, start_game)

    def setup_ui(self, root, ui_builder, saved_data, start_game):
        container = tk.Frame(self.window, bg=self.styles['frame_bg'], padx=20, pady=20)
        container.pack(expand=True, fill=tk.BOTH)

        empty_cells = sum(row.count(0) for row in saved_data['puzzle'])
        total_seconds = saved_data.get('timer', 0)
        minutes, seconds = divmod(total_seconds, 60)
        time_str = f"{minutes:02}:{seconds:02}"

        btn_text = (f"Difficulty: {saved_data.get('difficulty')}\n"
                    f"Time: {time_str}\n"
                    f"Empty Cells: {empty_cells}")

        btn = tk.Button(
            container,
            text=btn_text,
            command=lambda: self.on_save_selected(saved_data, self.window, start_game),
            **self.styles['button_style']
        )
        btn.pack(fill=tk.X, pady=5)

        tk.Button(
            container,
            text="Cancel",
            command=self.window.destroy,
            **self.styles['button_style']
        ).pack(fill=tk.X, pady=5)

    @staticmethod
    def on_save_selected(saved_data, save_window, start_game):
        save_window.destroy()
        start_game(
            difficulty=saved_data.get('difficulty'),
            loaded_data=saved_data
        )


class MainMenu:
    def __init__(self, root, frame_bg, button_style, autosave_manager,
                 start_callback=None, continue_callback=None):
        self.root = root
        self.frame_bg = frame_bg
        self.button_style = button_style
        self.start_callback = start_callback
        self.continue_callback = continue_callback
        self.autosave_manager = autosave_manager
        self.setup_ui()
        self.continue_btn = None

    def setup_ui(self):
        self.clear_window()
        self.root.title("Sudoku Main Menu")
        self.root.geometry("300x200")
        self.root.minsize(300, 200)

        frame = tk.Frame(self.root, bg=self.frame_bg, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="Sudoku Game",
                 font=('Arial', 14, 'bold'), bg=self.frame_bg).pack(pady=10)

        tk.Button(
            frame,
            text="New Game",
            command=self.on_start,
            **self.button_style
        ).pack(pady=8)

        self.continue_btn = tk.Button(
            frame,
            text="Continue",
            state='normal' if self.autosave_manager.load() else 'disabled',
            command=self.on_continue,
            **self.button_style
        )
        self.continue_btn.pack(pady=8)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_start(self):
        if self.start_callback:
            self.start_callback()

    def on_continue(self):
        if self.continue_callback:
            self.continue_callback()


class DifficultySelector:
    def __init__(self, root, difficulties, frame_bg, button_style, callback):
        self.root = root
        self.difficulties = difficulties
        self.frame_bg = frame_bg
        self.button_style = button_style
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.root.title("Sudoku Difficulty")
        self.root.geometry("300x200")
        self.root.minsize(300, 200)

        frame = tk.Frame(self.root, bg=self.frame_bg, padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="Choose Difficulty",
                 font=('Arial', 14), bg=self.frame_bg).pack(pady=5)

        for diff in self.difficulties:
            btn = tk.Button(
                frame,
                text=diff,
                command=lambda d=diff: self.on_difficulty_selected(d),
                **self.button_style
            )
            btn.pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_difficulty_selected(self, difficulty):
        self.callback(difficulty)