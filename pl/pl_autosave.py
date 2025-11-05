# pl/pl_autosave.py
def deserialize(data: dict) -> dict:
    """
    Normalize legacy save shapes into canonical payload.
    Ensures integers in puzzle and presence of cell_types.
    """
    payload = dict(data)  # shallow copy
    if 'puzzle' in payload:
        new_puzzle = []
        for row in payload['puzzle']:
            new_row = []
            for cell in row:
                s = str(cell).strip()
                new_row.append(0 if s in ('', '0') else int(s))
            new_puzzle.append(new_row)
        payload['puzzle'] = new_puzzle

    if 'cell_types' not in payload:
        cell_types = []
        for row in payload['puzzle']:
            ct_row = ['text' if cell == 0 else 'label' for cell in row]
            cell_types.append(ct_row)
        payload['cell_types'] = cell_types

    payload.setdefault('hints_remaining', 5)
    payload.setdefault('timer', 0)
    payload.setdefault('validation_mode', 'v1')
    return payload

def serialize(core_game, timer, difficulty: str, validation_mode: str, cell_types):
    # Optional helper; kept for completeness
    return {
        'puzzle': core_game.to_dict()['puzzle'],
        'solution': core_game.to_dict()['solution'],
        'hints_remaining': getattr(core_game, 'hints_remaining', 5),
        'timer': timer.elapsed() if timer else 0,
        'difficulty': difficulty,
        'validation_mode': validation_mode,
        'cell_types': cell_types
    }