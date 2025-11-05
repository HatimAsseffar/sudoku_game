def clear_window(self):
    for widget in self.root.winfo_children():
        widget.destroy()

# utils.py

def get_ui_styles(validate_callback=None, hint_callback=None,
                  new_game_callback=None, menu_callback=None,
                  hints_remaining=5):
    return {
        'font': ('Arial', 20),
        'cell_bg': 'white',
        'frame_bg': '#F0F0F0',
        'button_style': {
            'font': ('Garamond', 12),
            'bg': '#4CAF50',
            'fg': 'white',
            'activebackground': '#45a049',
            'width': 10
        },
        'hint_callback': hint_callback,
        'new_game_callback': new_game_callback,
        'menu_callback': menu_callback,
        'hints_remaining': hints_remaining,
        'validate_callback': validate_callback
    }

def is_victory(entries):
    alive_entries = [e for e in entries if e.winfo_exists()]
    return all(e.get().strip() == str(e.expected) for e in alive_entries)