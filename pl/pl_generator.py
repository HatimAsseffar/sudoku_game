                    
import random
from typing import List, Tuple, Optional


class SudokuGenerator:
    """
    Pure core Sudoku generator (moved from GUI module).
    Public API:
      - generate_puzzle(holes: int) -> List[List[int]]  # returns puzzle with holes removed
      - self.solution: List[List[int]]                  # full solved grid after generation
    """

    def __init__(self):
        self.grid: List[List[int]] = []
        self.solution: Optional[List[List[int]]] = None
        self.reset_grid()

    def reset_grid(self) -> None:
        self.grid = [[0] * 9 for _ in range(9)]
        self.solution = None

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Return True if placing num at (row,col) does not break Sudoku rules."""
        if num in self.grid[row]:
            return False
        if num in (self.grid[r][col] for r in range(9)):
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c] == num:
                    return False
        return True

    def find_empty(self) -> Optional[Tuple[int, int]]:
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def solve(self) -> bool:
        """Backtracking solver that fills self.grid in-place. Returns True if solved."""
        empty = self.find_empty()
        if not empty:
            return True
        r, c = empty
        for num in random.sample(range(1, 10), 9):
            if self.is_valid(r, c, num):
                self.grid[r][c] = num
                if self.solve():
                    return True
                self.grid[r][c] = 0
        return False

    def generate_full_grid(self, max_attempts: int = 10) -> None:
        """
        Create a fully solved grid.

        Strategy:
          - Seed the three diagonal 3x3 boxes with random permutations of 1..9.
          - Run the backtracking solver to fill the rest.
          - Retry the whole process up to max_attempts times if solving fails.
        """
        for attempt in range(max_attempts):
            self.reset_grid()
                                                           
            for box_start in (0, 3, 6):
                nums = list(range(1, 10))
                random.shuffle(nums)
                idx = 0
                for i in range(3):
                    for j in range(3):
                        self.grid[box_start + i][box_start + j] = nums[idx]
                        idx += 1

                                                                                
            if self.solve():
                                                                    
                self.solution = [row.copy() for row in self.grid]
                return

                                                                                      
        raise RuntimeError("SudokuGenerator: failed to generate a full valid grid after retries")

    def create_puzzle(self, holes: int = 10) -> List[List[int]]:
        """Copy solved solution to puzzle and remove `holes` random cells (set them to 0)."""
        if self.solution is None:
                                                                        
            self.generate_full_grid()
                                                    
        puzzle = [row.copy() for row in self.solution]
        all_cells = [(r, c) for r in range(9) for c in range(9)]
        cells_to_clear = random.sample(all_cells, min(len(all_cells), max(0, holes)))
        for r, c in cells_to_clear:
            puzzle[r][c] = 0
                                                                             
        self.grid = [row.copy() for row in puzzle]
        return [row.copy() for row in self.grid]

    def generate_puzzle(self, holes: int) -> List[List[int]]:
        """High-level helper: generate full grid then remove holes and return puzzle."""
        self.reset_grid()
        self.generate_full_grid()
        return self.create_puzzle(holes)