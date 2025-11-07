             
class GameTimer:
    def __init__(self, initial_seconds: int = 0):
        self._seconds = initial_seconds
        self.running = False

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    def tick(self, seconds: int = 1) -> None:
        if self.running:
            self._seconds += seconds

    def elapsed(self) -> int:
        return self._seconds

    def to_dict(self) -> dict:
        return {'elapsed': self._seconds}

    @staticmethod
    def from_dict(data: dict) -> "GameTimer":
        return GameTimer(initial_seconds=int(data.get('elapsed', 0)))