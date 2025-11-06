from adpt.game_state_loader_adapter import restore_from_payload


class GameStateLoader:
    @staticmethod
    def restore(loaded_data):
        if not loaded_data:
            return None
        return restore_from_payload(loaded_data)