from enum import Enum

class TaskType(Enum):
    VPU = 'vector task'
    ME = 'matrix task'
    FE = 'activation task'

class Task:
    def __init__(self, addr_start, addr_end, task_type):
        self.addr_start = addr_start
        self.addr_end = addr_end
        self.task_type = task_type

    def get_task_type(self):
        return self.task_type

    def get_addr_start(self):
        return self.addr_start

    def get_addr_end(self):
        return self.addr_end