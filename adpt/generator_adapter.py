# adpt/generator_adapter.py
from typing import Dict, List
from pl.pl_generator import SudokuGenerator


class GeneratorAdapter:
    """
    Small adapter wrapping pl.pl_generator.SudokuGenerator to expose a simple,
    canonical generator API used by the GUI layer.
    Public method:
      - generate(holes: int) -> {'puzzle': List[List[int]], 'solution': List[List[int]]}
    """

    def __init__(self):
        self._gen = SudokuGenerator()

    def generate(self, holes: int = 10) -> Dict[str, List[List[int]]]:
        """
        Generate a puzzle with `holes` empty cells.
        Returns a canonical payload with 'puzzle' and 'solution' keys.
        """
        puzzle = self._gen.generate_puzzle(holes)
        # generator keeps last solution in self._gen.solution
        solution = [row.copy() for row in (self._gen.solution or [[0]*9 for _ in range(9)])]
        return {
            'puzzle': [row.copy() for row in puzzle],
            'solution': solution
        }