from .Unit import Unit
from .Status import Status
from .Memory import Memory
from typing import TYPE_CHECKING, List, Tuple, Callable

if TYPE_CHECKING:
    from .Task import Task
    from .TPC import TPC
    from .TPC_Executor import TPC_Executor


class TPC_CU(Unit):
    def __init__(self, tpc: "TPC"):
        super().__init__(f"{tpc.name}_CU")
        self._queue: List["Task"] = []
        self._tpc = tpc
        self._noc: List[Tuple[int, int, "TPC_Executor" | None]] = []
        self._noc_ranges: List[Tuple[int, int]] = [] # удалить, использовать только _noc

    def get_queue_length(self) -> int:
        return len(self._queue)

    def add_task(self, task: "Task", callback_on_complete: Callable[["Task"], None]):
        self._queue.append(task)

    def _on_complete_task(self, task: "Task"):
        pass

    def _is_in_noc(self, task: "Task") -> bool:
        for s, e in self._noc_ranges:
            if Memory._ranges_overlap(task.addr_start, task.addr_end, s, e):
                return True
        return False

    def _action(self):
        if not self._queue and not self._noc:
            self._set_status(Status.SEND_TO_GLOBAL)

        match self._status:
            case Status.WAIT:
                self._wait()
            case Status.SEND_TO_GLOBAL:
                self._send_to_global()
            case Status.COLLECT_TO_LOCAL:
                self._load_from_global()
            case Status.SEND_TO_EXECUTE:
                self._send_to_executor()

    def _wait(self):
        if not self._queue:
            return

        task = self._queue[0]
        if not self._is_in_noc(task):
            self._set_status(Status.COLLECT_TO_LOCAL)
        else:
            self._set_status(Status.SEND_TO_EXECUTE)

    def _load_from_global(self):
        task = self._queue[0]
        if (task.addr_start, task.addr_end) not in self._noc_ranges:
            self._noc_ranges.append((task.addr_start, task.addr_end))
        self._set_status(Status.SEND_TO_EXECUTE)

    def _send_to_global(self):
        if self._noc_ranges:
            start, end = self._noc_ranges.pop(0)
            Memory.release(self._noc, start, end, None)
        self._set_status(Status.WAIT)

    def _send_to_executor(self):
        task = self._queue[0]
        executor = self._tpc.get_executor(task.task_type)
        executor.set_active_task(task)

        if  Memory.check_conflict(self._noc, task.addr_start, task.addr_end, executor):
            return
        
        Memory.allocate(self._noc, task.addr_start, task.addr_end, executor)
        self._queue.pop(0)
        self._set_status(Status.WAIT)
