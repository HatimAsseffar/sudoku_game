import tkinter as tk
from tkinter import messagebox

                                                       
from pl.pl_game import CoreGame
from pl.pl_timer import GameTimer
from adpt.generator_adapter import GeneratorAdapter
from adpt.validation_adapter import ValidationAdapter
from adpt.hint_adapter import HintAdapter
from adpt.timer_adapter import TimerAdapter
from adpt.autosave_adapter import AutosaveAdapter
from adpt.game_state_loader_adapter import restore_from_payload

from ui import SudokuUIBuilder
from utils import get_ui_styles
from VicMsg import show_victory
from menu_manager import MenuManager


class SudokuGame:
    DIFFICULTIES = {'Easy': 25, 'Medium': 39, 'Hard': 50}

    def __init__(self, root=None):
        self.root = root or tk.Tk()

                                 
        self.generator_adapter = GeneratorAdapter()
        self.core_game = None                                     
        self.game_timer = None                                     
        self.timer_adapter = None                                       
        self.validation_adapter = None                                      
        self.hint_adapter = None                                      
        self.autosave_adapter = AutosaveAdapter()
            
        self.styles = get_ui_styles(
            validate_callback=None,
            hint_callback=None,
            new_game_callback=None,
            menu_callback=None,
            hints_remaining=5
        )
        self.menu_manager = MenuManager(self, self.root, styles=self.styles)
        self.ui_builder = SudokuUIBuilder(self.root, self.styles, game=self)
                                                                         
        try:
            self.ui_builder.rebind_control_callbacks(
                new_game_callback=lambda: self.menu_manager.on_start_new_game(),
                menu_callback=lambda: self.menu_manager.show_main_menu(),
                hint_callback=lambda: self.give_hint()
            )
        except Exception:
                                                                                    
            pass
                   
        self.current_difficulty = None
        self.starting_new_game = False

                         
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_with_save)

                                         
    def start(self):
        self.menu_manager.show_main_menu()
        if not self.root.winfo_viewable():
            self.root.mainloop()

    def show_difficulty_selector(self):
        self.menu_manager.show_difficulty_selector()

                                                       
    def start_game(self, difficulty, loaded_data=None):
        """Begin a new game or restore a loaded one."""
        self.current_difficulty = difficulty
        self.prepare_window()
        self.prepare_game_data(loaded_data)
        self.update_hint_button()

    def prepare_window(self):
        """Clear existing UI and reset window properties."""
        self.clear_window()
        self.root.title("Sudoku")
        self.root.geometry("450x500")
        self.root.minsize(450, 500)

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    def prepare_game_data(self, loaded_data=None):
        """
        Initialize core_game, timer and adapters.
        If loaded_data is provided it is a normalized payload returned by AutosaveAdapter.load().
        """
                                                            
        self.ui_builder.cells = [[None for _ in range(9)] for _ in range(9)]
        self.ui_builder.current_entries = []

        if loaded_data:
                                                             
            payload = restore_from_payload(loaded_data) if not loaded_data.get('core_game') else loaded_data
                                                                                                                                
            puzzle = payload['puzzle']
            solution = payload['solution']

                                                   
            self.core_game = CoreGame(puzzle, solution)
                                                               
            if 'hints_remaining' in payload:
                try:
                    self.core_game.hints_remaining = int(payload.get('hints_remaining', self.core_game.hints_remaining))
                except Exception:
                    pass

            self.game_timer = GameTimer.from_dict({'elapsed': int(payload.get('timer', 0))})
            self.validation_mode_on_load = payload.get('validation_mode', 'v1')
            cell_types = payload.get('cell_types', None)

                                        
            self.generate_game_ui(cell_types=cell_types, loaded_payload=payload)
                                       
            if self.timer_adapter:
                self.timer_adapter.start()
        else:
                                                             
            holes = self.DIFFICULTIES.get(self.current_difficulty, 25)
            payload = self.generator_adapter.generate(holes)
            puzzle = payload['puzzle']
            solution = payload['solution']

                                         
            self.core_game = CoreGame(puzzle, solution)
            self.core_game.hints_remaining = 5
            self.game_timer = GameTimer(initial_seconds=0)

                                        
            self.generate_game_ui(cell_types=None, loaded_payload=None)
                                                                                 
            self.timer_adapter.start()

    def update_hint_button(self):
        """If a hint adapter exists and a hint button is present, ensure the button text/state is correct."""
        if self.hint_adapter and hasattr(self.hint_adapter, 'button') and self.hint_adapter.button:
            self.hint_adapter._update_button()                                                    

                                                            
    def generate_game_ui(self, cell_types=None, loaded_payload=None):
        """
        Build the UI from self.core_game state and wire adapters.
        cell_types: optional 9x9 grid marking 'text'/'label' for each cell
        loaded_payload: optional canonical payload dict (used for restoring timer/validation mode)
        """
        puzzle = [row.copy() for row in self.core_game.board.puzzle] if hasattr(self.core_game, 'board') else self.core_game.to_dict()['puzzle']
        solution = [row.copy() for row in self.core_game.board.solution] if hasattr(self.core_game, 'board') else self.core_game.to_dict()['solution']

                                                                                                      
        hint_button, main_frame = self.ui_builder.create_game_ui(puzzle, solution, cell_types)

                                      
        self.hint_adapter = HintAdapter(self.core_game, self.ui_builder)
        self.hint_adapter.set_button(hint_button)

                                                                    
        self.validation_adapter = ValidationAdapter(self.core_game, self.ui_builder, initial_mode=getattr(self, 'validation_mode_on_load', 'v1'))
        self.ui_builder.register_input_handler(self._wrap_validation_handler())

                                                                                                      
        self.timer_adapter = TimerAdapter(self.root, self.game_timer)
                                                            
        self.ui_builder.add_timer_label(main_frame, self.timer_adapter)

        self.ui_builder.rebind_control_callbacks(
            new_game_callback=self.prompt_new_game,
            menu_callback=self.show_settings_window,
            hint_callback=self.give_hint
        )

                                                                        
                                                                    

    def _wrap_validation_handler(self):
        """Return a callable matching UI handler signature (row, col, text) that forwards to validation adapter."""
        def handler(row, col, text):
            if not self.validation_adapter:
                return True
            result = self.validation_adapter.handle_input(row, col, text)
                                                                                    
            try:
                if self.core_game.is_complete():
                                                                                      
                    if all(self.core_game.is_correct(r, c) for r in range(9) for c in range(9)):
                                                     
                        if self.timer_adapter:
                            self.timer_adapter.stop()
                        show_victory(self.root)
            except Exception:
                                                                               
                pass
            return result
        return handler

                                                                           
    def give_hint(self):
        if self.hint_adapter:
            self.hint_adapter.on_request_hint()
            self.update_hint_button()

                                                  
    def save_game(self):
        """Explicit save using adapters: delegate to AutosaveAdapter."""
        try:
            cell_types_callable = self.ui_builder.get_cell_types
            self.autosave_adapter.save(
                core_game=self.core_game,
                timer=self.game_timer,
                difficulty=self.current_difficulty,
                validation_mode=(self.validation_adapter.mode if self.validation_adapter else 'v1'),
                ui_get_cell_types=cell_types_callable
            )
        except Exception as e:
            print(f"Failed to save game via adapter: {e}")

    def load_game(self):
        """Load normalized payload from autosave adapter and return it (GUI caller will restore)."""
        return self.autosave_adapter.load()

                                                                    
    def check_victory(self):
        if not self.core_game:
            return
        if self.core_game.is_complete() and all(self.core_game.is_correct(r, c) for r in range(9) for c in range(9)):
            if self.timer_adapter:
                self.timer_adapter.stop()
            show_victory(self.root)

                                             
    def prompt_new_game(self):
        response = messagebox.askyesno("New Game", "Would you like to change difficulty?", icon='question')
        if response:
            self.menu_manager.show_difficulty_selector()
        else:
            if self.current_difficulty:
                self.starting_new_game = True
                self.start_game(self.current_difficulty)

                                         
    def show_settings_window(self):
        self.menu_manager.show_settings_window()

                                           
    def on_close(self):
        """Clean exit without redundant prompts."""
        try:
            if self.timer_adapter:
                self.timer_adapter.stop()
        finally:
            self.root.destroy()

    def on_close_with_save(self):
        """Prompt save on exit then close."""
        response = messagebox.askyesno("Save Progress", "Would you like to save your current game before exiting?", icon='question')
        if response:
            self.save_game()
        self.on_close()


if __name__ == "__main__":
    game = SudokuGame()
    game.start()