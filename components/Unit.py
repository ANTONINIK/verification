from abc import ABC, abstractmethod
from .Status import Status


class Unit(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self._status: Status = Status.WAIT
        self._ticker: int = self._status.value

    def tick(self):
        if self._ticker == 0:
            self._action()
        else:
            self._ticker -= 1

    def get_status(self):
        return self._status

    def _set_status(self, status: Status):
        self._status = status
        self._ticker = status.value

    @abstractmethod
    def _action(self):
        pass

    def __str__(self):
        return f"\t{self.name}: status = {self._status}, ticker = {self._ticker}"
