from abc import ABC, abstractmethod
from .Status import Status

class Tick(ABC):
    def __init__(self):
        self.status = Status.WAIT
        self.ticker = self.status.value

    @abstractmethod
    def _action(self):
        pass

    def _set_status(self, status):
        self.status = status
        self.ticker = self.status.value

    def tick(self):
        if self.ticker == 0:
            self._action()
        else:
            self.ticker -= 1

    def print_status(self):
        return f'status = {self.status}, ticker = {self.ticker}'