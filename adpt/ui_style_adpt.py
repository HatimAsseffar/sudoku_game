def get_ui_styles(validate_callback, hint_callback, new_game_callback, menu_callback):
    return {
        'frame_bg': '#f0f0f0',
        'button_style': {
            'font': ('Arial', 12),
            'bg': '#e0e0e0',
            'activebackground': '#d0d0d0',
            'relief': 'raised'
        },
        'validate_callback': validate_callback,
        'hint_callback': hint_callback,
        'new_game_callback': new_game_callback,
        'menu_callback': menu_callback
    }
