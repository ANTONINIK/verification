from .Unit import Unit
from .TaskType import TaskType
from .TPC_CU import TPC_CU
from .TPC_Executor import TPC_Executor
from typing import TYPE_CHECKING, Callable
from .BColors import BColors

if TYPE_CHECKING:
    from .Task import Task


class TPC(Unit):
    def __init__(self, name: str):
        super().__init__(name, BColors.OKGREEN, 1)
        self._VPU_executor = TPC_Executor(self, TaskType.VPU)
        self._ME_executor = TPC_Executor(self, TaskType.ME)
        self._FE_executor = TPC_Executor(self, TaskType.FE)
        self._TPC_CU = TPC_CU(self)
        self._current_tick = 0  # Track current tick

    def set_current_tick(self, tick: int):
        self._current_tick = tick
        self._VPU_executor._current_tick = tick
        self._ME_executor._current_tick = tick
        self._FE_executor._current_tick = tick

    def get_total_task_count(self) -> int:
        return self._TPC_CU.get_queue_length()

    def add_task(self, task: "Task", callback_on_complete: Callable[["Task"], None]):
        self._TPC_CU.add_task(task, callback_on_complete)

    def _action(self):
        self._TPC_CU.tick()
        self._VPU_executor.tick()
        self._ME_executor.tick()
        self._FE_executor.tick()

    def __str__(self):
        return f"{super().__str__()}\n{f"{self._VPU_executor}"}\n{f"{self._ME_executor}"}\n{f"{self._FE_executor}"}\n{f"{self._TPC_CU}"}"
