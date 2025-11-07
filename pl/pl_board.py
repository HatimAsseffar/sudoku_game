class GameBoard:
    def __init__(self, puzzle, solution):
        self.puzzle = [row.copy() for row in puzzle]
        self.solution = [row.copy() for row in solution]

    def get_value(self, row, col):
        return self.puzzle[row][col]

    def set_value(self, row, col, value):
        self.puzzle[row][col] = value

    def is_complete(self):
        """Return True if all cells are filled (non-zero)."""
        return all(self.puzzle[r][c] != 0 for r in range(9) for c in range(9))

    def is_correct(self, row, col):
        """Return True if the value at row,col matches solution."""
        return self.puzzle[row][col] == self.solution[row][col]

    def empty_cells(self):
        """Return list of (row, col) for empty cells."""
        return [(r, c) for r in range(9) for c in range(9) if self.puzzle[r][c] == 0]

    def _none(self):
        return
