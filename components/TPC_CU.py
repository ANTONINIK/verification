from .Unit import Unit
from .Status import Status
from .Memory import Memory
from .TaskType import TaskType
from .BColors import BColors
from typing import TYPE_CHECKING, List, Tuple, Callable, Dict

if TYPE_CHECKING:
    from .Task import Task
    from .TPC import TPC
    from .TPC_Executor import TPC_Executor


class TPC_CU(Unit):
    def __init__(self, tpc: "TPC"):
        super().__init__(f"{tpc.name}_CU", BColors.WARNING, 2)
        self._queue: List["Task"] = []
        self._tpc: "TPC" = tpc
        self._noc: List[Tuple[int, int, "TPC_Executor" | None]] = []
        self._callback_on_complete_by_task: Dict["Task", Callable[["Task"], None]] = {}

    def get_queue_length(self) -> int:
        return len(self._queue)

    def add_task(self, task: "Task", callback_on_complete: Callable[["Task"], None]):
        self.log(f"Adding {task} to CU queue")
        self._queue.append(task)
        self._callback_on_complete_by_task[task] = callback_on_complete

    def _on_complete_task(self, task: "Task"):
        self.log(f"Releasing memory for completed task {task}")
        Memory.release(self._noc, task.addr_start, task.addr_end)
        self._callback_on_complete_by_task.pop(task, None)(task)

    def _is_in_noc(self, task: "Task") -> bool:
        return Memory.is_contained(self._noc, task.addr_start, task.addr_end)

    def _action(self):
        self.log(f"Queue length: {len(self._queue)}")

        if not self._queue and self._noc:
            self.set_status(Status.SEND_TO_GLOBAL)

        match self._status:
            case Status.WAIT:
                self._wait()
            case Status.SEND_TO_GLOBAL:
                self._send_to_global()
            case Status.COLLECT_TO_LOCAL:
                self._collect_to_local()

    def _wait(self):
        self.log("Checking for tasks in CU queue")

        if not self._queue:
            self.log("No tasks in queue")
            return

        task = self._queue[0]
        if not self._is_in_noc(task):
            self.set_status(Status.COLLECT_TO_LOCAL)
            return

        task = self._queue[0]
        executor = self._get_executor(task.task_type)

        if Memory.check_conflict(self._noc, task.addr_start, task.addr_end, executor):
            self.log("Memory conflict detected")
            return

        if executor.get_active_task() is not None:
            self.log("Executor is busy")
            return

        Memory.allocate(self._noc, task.addr_start, task.addr_end, executor)
        executor.set_active_task(self._queue.pop(0), self._on_complete_task)
        self.set_status(Status.WAIT)

    def _collect_to_local(self):
        task = self._queue[0]
        self.log(f"Loading {task} from global memory")
        self._noc.append((task.addr_start, task.addr_end, None))
        self.set_status(Status.WAIT)

    def _send_to_global(self):
        self.log("Sending task results to global memory")
        if self._noc:
            start, end, _ = self._noc.pop(0)
            Memory.release(self._noc, start, end)
        self.set_status(Status.WAIT)

    def _get_executor(self, task_type: "TaskType") -> "TPC_Executor":
        match task_type:
            case TaskType.VPU:
                return self._tpc._VPU_executor
            case TaskType.ME:
                return self._tpc._ME_executor
            case TaskType.FE:
                return self._tpc._FE_executor
