from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .TaskType import TaskType
    from .TPC import TPC

class Task:
    _id = 1

    def __init__(self, addr_start: int, addr_end: int, task_type: "TaskType"):
        self.id = Task._id
        Task._id += 1
        self.addr_start = addr_start
        self.addr_end = addr_end
        self.task_type = task_type
        self.is_completed = False
        self.start_time: Optional[int] = None
        self.end_time: Optional[int] = None
        self.executed_by: Optional[str] = None
        self.assigned_tpc: Optional["TPC"] = None

    @property
    def latency(self) -> Optional[int]:
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        latency_str = f", latency={self.latency}" if self.latency is not None else ""
        exec_str = f", executed_by={self.executed_by}" if self.executed_by is not None else ""
        return (f"Task(id={self.id}, task_type={self.task_type}, "
                f"addr_start={self.addr_start}, addr_end={self.addr_end}, "
                f"is_completed={self.is_completed}{latency_str}{exec_str})")
