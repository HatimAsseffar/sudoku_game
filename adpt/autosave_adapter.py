# adpt/autosave_adapter.py
import json
import os
from typing import Callable, Optional, Dict
from pl.pl_autosave import deserialize, serialize  # pl serializer/deserializer if present

class AutosaveAdapter:
    def __init__(self, save_path: str = "sudoku_autosave.json"):
        self.save_path = save_path

    def save(self, core_game, timer, difficulty: str, validation_mode: str, ui_get_cell_types: Callable[[], list]):
        payload = {
            'puzzle': core_game.to_dict()['puzzle'],
            'solution': core_game.to_dict()['solution'],
            'hints_remaining': getattr(core_game, 'hints_remaining', 5),
            'timer': timer.elapsed() if timer else 0,
            'difficulty': difficulty,
            'validation_mode': validation_mode,
            'cell_types': ui_get_cell_types()
        }
        with open(self.save_path, 'w') as f:
            json.dump(payload, f, indent=2)

    def load(self) -> Optional[Dict]:
        try:
            with open(self.save_path, 'r') as f:
                data = json.load(f)
            # Delegate normalization to pl.pl_autosave.deserialize if available
            try:
                normalized = deserialize(data)  # pl-level normalizer
                return normalized
            except Exception:
                # fallback normalization if pl.pl_autosave not available
                if 'puzzle' in data:
                    # ensure integers and cell_types
                    puzzle = []
                    for row in data['puzzle']:
                        new_row = []
                        for cell in row:
                            s = str(cell).strip()
                            new_row.append(0 if s in ('', '0') else int(s))
                        puzzle.append(new_row)
                    data['puzzle'] = puzzle
                if 'cell_types' not in data:
                    cell_types = []
                    for row in data['puzzle']:
                        cell_types.append(['text' if cell == 0 else 'label' for cell in row])
                    data['cell_types'] = cell_types
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def clear(self):
        try:
            os.remove(self.save_path)
        except FileNotFoundError:
            pass