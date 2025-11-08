from .Tick import Tick
from .Status import Status
from .Task import TaskType

class TPC_Executor(Tick):
    def __init__(self, task_type):
        super().__init__()
        self.task_type = task_type
        self.active_task = None

    def add_task(self, task):
        self.active_task = task

    def _action(self):
        print(f'TPC_Executor {self.task_type.value}: action')
        if self.active_task:
            print('Start executing task')
            if self.task_type != self.active_task.task_type:
                print('Wrong task type! This executor cant work with that task type')
            else:
                match self.task_type:
                    case TaskType.VPU:
                        self._set_status(Status.EXEC_VPU)
                    case TaskType.ME:
                        self._set_status(Status.EXEC_ME)
                    case TaskType.FE:
                        self._set_status(Status.EXEC_FE)
                    case _:
                        print("Unknown task type")

    def __str__(self):
        status = self.print_status()
        return f'TCP_Executor {self.task_type.value}: {status}'