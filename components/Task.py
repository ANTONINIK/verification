from enum import Enum

class TaskType(Enum):
    VPU = 'vector'
    ME = 'matrix'
    FE = 'activation'

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

    def __str__(self):
        return f'task: task_type = {self.task_type}, addr_start = {self.addr_start}, addr_end = {self.addr_end}'