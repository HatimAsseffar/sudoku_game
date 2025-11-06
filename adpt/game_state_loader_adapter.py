def restore_from_payload(payload: dict):
    """
    Accepts canonical payload (as produced by AutosaveAdapter.load) or older shapes.
    Returns canonical payload dict ensuring keys puzzle, solution, hints_remaining, timer, difficulty, validation_mode, cell_types.
    """
    data = {
        'puzzle': payload.get('puzzle'),
        'solution': payload.get('solution'),
        'hints_remaining': payload.get('hints_remaining', 5),
        'timer': payload.get('timer', 0),
        'difficulty': payload.get('difficulty'),
        'validation_mode': payload.get('validation_mode', 'v1'),
        'cell_types': payload.get('cell_types')
    }
    return data