from abc import ABC, abstractmethod
from .Status import Status
from .BColors import BColors

TICK_COUNT_BY_STATUS = {
    Status.WAIT: 0,
    Status.COLLECT_TO_LOCAL: 2,
    Status.SEND_TO_GLOBAL: 2,
    Status.EXEC_VPU: 3,
    Status.EXEC_ME: 3,
    Status.EXEC_FE: 3,
}

ENABLE_LOGGING = True

class Unit(ABC):
    def __init__(self, name: str, color: str, level: int = 0):
        self.name: str = name
        self.color: str = color
        self.level: int = level
        self._status: Status = Status.WAIT
        self._ticker: int = TICK_COUNT_BY_STATUS[self._status]

    def log(self, message: str):
        if ENABLE_LOGGING:
            print(f"{self.color}{'\t' * self.level}{self.name}: {message}{BColors.ENDC}")

    def tick(self):
        if self._ticker < 1:
            self._action()
        else:
            self._ticker -= 1

    def get_status(self):
        return self._status

    def set_status(self, status: Status):
        self._status = status
        self._ticker = TICK_COUNT_BY_STATUS.get(status)

    @abstractmethod
    def _action(self):
        pass

    def __str__(self):
        return f"{'\t' * self.level}{self.name}: status={self._status.name}, ticker={self._ticker}"
