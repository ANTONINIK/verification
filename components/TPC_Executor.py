from .Unit import Unit
from .Status import Status

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .TaskType import TaskType
    from .TPC import TPC


class TPC_Executor(Unit):
    def __init__(self, tpc: "TPC", task_type: "TaskType"):
        super().__init__(f"{tpc.name}_Executor")
        self._tpc = tpc
        self._task_type = task_type
        self._active_task = None

    def get_active_task(self):
        return self._active_task

    def set_active_task(self, task):
        self._active_task = task

    def _action(self):
        if not self._active_task:
            return

        match self._task_type:
            case TaskType.VPU:
                self._set_status(Status.EXEC_VPU)
            case TaskType.ME:
                self._set_status(Status.EXEC_ME)
            case TaskType.FE:
                self._set_status(Status.EXEC_FE)
