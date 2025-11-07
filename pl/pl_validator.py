                 
from typing import Callable, List, Tuple

BoardGetter = Callable[[int,int], int]

def is_row_valid(board_getter: BoardGetter, num: int, row: int, col: int) -> bool:
    return all(board_getter(row, c) != num for c in range(9) if c != col)

def is_col_valid(board_getter: BoardGetter, num: int, row: int, col: int) -> bool:
    return all(board_getter(r, col) != num for r in range(9) if r != row)

def is_section_valid(board_getter: BoardGetter, num: int, row: int, col: int) -> bool:
    sr, sc = 3*(row//3), 3*(col//3)
    return all(board_getter(r, c) != num
               for r in range(sr, sr+3) for c in range(sc, sc+3)
               if not (r == row and c == col))

def valid_for(board_getter: BoardGetter, num: int, row: int, col: int) -> bool:
    return (is_row_valid(board_getter, num, row, col) and
            is_col_valid(board_getter, num, row, col) and
            is_section_valid(board_getter, num, row, col))

def find_conflicts(board_getter: BoardGetter, row: int, col: int) -> List[Tuple[int,int]]:
    conflicts = []
    val = board_getter(row, col)
    if val == 0:
        return conflicts
    for c in range(9):
        if c != col and board_getter(row, c) == val:
            conflicts.append((row, c))
    for r in range(9):
        if r != row and board_getter(r, col) == val:
            conflicts.append((r, col))
    sr, sc = 3*(row//3), 3*(col//3)
    for r in range(sr, sr+3):
        for c in range(sc, sc+3):
            if (r, c) != (row, col) and board_getter(r, c) == val:
                conflicts.append((r, c))
    return conflicts