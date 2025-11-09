from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .TaskType import TaskType

class Task:
    _id = 1

    def __init__(self, addr_start: int, addr_end: int, task_type: "TaskType"):
        self.id = Task._id
        Task._id += 1
        self.addr_start = addr_start
        self.addr_end = addr_end
        self.task_type = task_type
        self.is_completed = False

    def __str__(self):
        return (f"Task(id={self.id}, task_type={self.task_type}, "
                f"addr_start={self.addr_start}, addr_end={self.addr_end}, "
                f"is_completed={self.is_completed})")
