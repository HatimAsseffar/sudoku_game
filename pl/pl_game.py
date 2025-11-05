# pl_game.py
from typing import Callable, List, Tuple, Optional
from pl.pl_board import GameBoard
import random

class CoreGame:
    def __init__(self, puzzle: List[List[int]], solution: List[List[int]]):
        self.board = GameBoard(puzzle, solution)
        self.hints_remaining = 5
        self._on_cell_changed: List[Callable[[int,int,int], None]] = []
        self._on_victory: List[Callable[[], None]] = []

    def set_cell(self, row: int, col: int, value: int) -> None:
        self.board.set_value(row, col, value)
        for cb in self._on_cell_changed:
            cb(row, col, value)
        if self.board.is_complete() and all(
            self.board.is_correct(r, c) for r in range(9) for c in range(9)
        ):
            for cb in self._on_victory:
                cb()

    def get_cell(self, row: int, col: int) -> int:
        return self.board.get_value(row, col)

    def empty_cells(self) -> List[Tuple[int,int]]:
        return self.board.empty_cells()

    def is_complete(self) -> bool:
        return self.board.is_complete()

    def is_correct(self, row:int, col:int) -> bool:
        return self.board.is_correct(row, col)

    def request_hint(self) -> Optional[Tuple[int,int,int]]:
        if self.hints_remaining <= 0:
            return None
        empties = self.empty_cells()
        if not empties:
            return None
        r, c = random.choice(empties)
        val = self.board.solution[r][c]
        self.board.set_value(r, c, val)
        self.hints_remaining -= 1
        for cb in self._on_cell_changed:
            cb(r, c, val)
        return (r, c, val)

    def register_on_cell_changed(self, callback: Callable[[int,int,int], None]) -> None:
        self._on_cell_changed.append(callback)

    def register_on_victory(self, callback: Callable[[], None]) -> None:
        self._on_victory.append(callback)

    def to_dict(self) -> dict:
        return {
            'puzzle': [row.copy() for row in self.board.puzzle],
            'solution': [row.copy() for row in self.board.solution],
            'hints_remaining': self.hints_remaining
        }

    @staticmethod
    def from_dict(data: dict) -> "CoreGame":
        cg = CoreGame(data['puzzle'], data['solution'])
        cg.hints_remaining = data.get('hints_remaining', 5)
        return cg

    @staticmethod
    def is_victory(entries):
        alive_entries = [e for e in entries if e.winfo_exists()]
        return all(e.get().strip() == str(e.expected) for e in alive_entries)