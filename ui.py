import tkinter as tk

class SudokuUIBuilder:
    def __init__(self, root, styles, game=None):
        self.root = root
        self.styles = styles
        self.game = game
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.current_entries = []
        self._input_handler = None

    def rebind_control_callbacks(self, new_game_callback=None, menu_callback=None, hint_callback=None):
        if new_game_callback and hasattr(self, '_new_button'):
            self._new_button.config(command=new_game_callback)
        if menu_callback and hasattr(self, '_menu_button'):
            self._menu_button.config(command=menu_callback)
        if hint_callback and hasattr(self, '_hint_button'):
            self._hint_button.config(command=hint_callback)

    def configure_grid_layout(self, parent):
        for i in range(9):
            parent.rowconfigure(i, weight=1, minsize=40)
            parent.columnconfigure(i, weight=1, minsize=40)

    def create_game_ui(self, puzzle, solution, cell_types=None):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        grid_frame = tk.Frame(main_frame)
        grid_frame.pack(pady=10)
        self.configure_grid_layout(grid_frame)

        self.create_game_cells(grid_frame, puzzle, solution, cell_types)
        hint_button, new_button, menu_button = self.create_control_buttons(main_frame)

        return hint_button, main_frame

    def create_game_cells(self, parent, puzzle, solution, cell_types):
        for row in range(9):
            for col in range(9):
                cell_value = puzzle[row][col]
                is_text_cell = self._determine_cell_type(cell_types, cell_value, row, col)

                cell_frame = self._create_cell_frame(parent, row, col)
                self._create_cell_widget(cell_frame, cell_value, row, col,
                                         is_text_cell, solution)

    def create_control_buttons(self, parent):
        button_frame = tk.Frame(parent)
        button_frame.pack(pady=10)

        self._hint_button = tk.Button(
            button_frame,
            text=f"Hint ({self.styles.get('hints_remaining', 0)})",
            **self.styles.get('button_style', {})
        )
        self._hint_button.pack(side=tk.LEFT, padx=5)

        self._new_button = tk.Button(
            button_frame,
            text="New Game",
            command=self.styles.get('new_game_callback'),
            **self.styles.get('button_style', {})
        )
        self._new_button.pack(side=tk.LEFT, padx=5)

        self._menu_button = tk.Button(
            button_frame,
            text="Menu",
            command=self.styles.get('menu_callback'),
            **self.styles.get('button_style', {})
        )
        self._menu_button.pack(side=tk.RIGHT, padx=5)

        return self._hint_button, self._new_button, self._menu_button

    def _determine_cell_type(self, cell_types, cell_value, row, col):
        if cell_types is not None:
            return cell_types[row][col] == 'text'
        return cell_value == 0

    def _create_cell_frame(self, parent, row, col):
        frame = tk.Frame(
            parent,
            bg=self.styles.get('cell_bg', 'white'),
            highlightthickness=0,
            borderwidth=1,
            relief='solid'
        )
        frame.grid(row=row, column=col, sticky='nsew')
        return frame

    def _create_cell_widget(self, cell_frame, cell_value, row, col,
                            is_text_cell, solution):
        if is_text_cell:
            entry = tk.Entry(
                cell_frame,
                font=self.styles.get('font'),
                width=2,
                justify='center',
                relief='flat',
                borderwidth=0,
                bg=self.styles.get('cell_bg', 'white'),
                validate='key',
                validatecommand=(self.root.register(self.validate_digit), "%P")
            )

            if cell_value != 0:
                entry.insert(0, str(cell_value))

            entry.expected = solution[row][col]
            entry.row, entry.col = row, col

                                                           
            def on_release(e, r=row, c=col, w=entry):
                if self._input_handler:
                    self._input_handler(r, c, w.get().strip())
            entry.bind("<KeyRelease>", on_release)

            entry.pack(expand=True, fill='both')
            self.current_entries.append(entry)
            self.cells[row][col] = entry
        else:
            label = tk.Label(
                cell_frame,
                text=str(cell_value) if cell_value != 0 else "",
                font=self.styles.get('font'),
                bg=self.styles.get('cell_bg', 'white'),
                width=2,
                justify='center'
            )
            label.pack(expand=True, fill='both')
            self.cells[row][col] = label

    def add_timer_label(self, frame, timer_adapter_or_var):
        """
        Accept either a TimerAdapter (with .time_var) or a tk.StringVar.
        """
        if hasattr(timer_adapter_or_var, 'time_var'):
            time_var = timer_adapter_or_var.time_var
        else:
            time_var = timer_adapter_or_var
        tk.Label(frame, textvariable=time_var, font=('Arial', 14), fg='blue').pack(pady=5)

    def validate_digit(self, proposed):
        return proposed == "" or (len(proposed) == 1 and proposed in "123456789")

                                                
    def get_widget(self, row, col):
        return self.cells[row][col]

    def get_cell_value(self, row, col):
        widget = self.get_widget(row, col)
        if isinstance(widget, tk.Entry):
            val = widget.get().strip()
            return int(val) if val else 0
        else:
            text = widget.cget('text')
            return int(text) if text else 0

    def set_cell_value(self, row, col, value):
        widget = self.get_widget(row, col)
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
            if value != 0:
                widget.insert(0, str(value))
        else:
            widget.config(text=str(value) if value != 0 else "")

    def set_cell_visual(self, row, col, **kwargs):
        widget = self.get_widget(row, col)
        widget.config(**kwargs)

    def get_cell_types(self):
        types = []
        for r in range(9):
            row_types = []
            for c in range(9):
                row_types.append('text' if isinstance(self.cells[r][c], tk.Entry) else 'label')
            types.append(row_types)
        return types

    def get_current_puzzle_state(self):
        state = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.get_cell_value(r, c))
            state.append(row)
        return state

    def register_input_handler(self, handler):
        """
        handler signature: func(row:int, col:int, text:str) -> bool
        Attach a handler used by all entry KeyRelease events.
        """
        self._input_handler = handler
                                                     
        for r in range(9):
            for c in range(9):
                w = self.cells[r][c]
                if isinstance(w, tk.Entry):
                    def on_release(e, rr=r, cc=c, ww=w):
                        if self._input_handler:
                            self._input_handler(rr, cc, ww.get().strip())
                    w.unbind("<KeyRelease>")
                    w.bind("<KeyRelease>", on_release)

