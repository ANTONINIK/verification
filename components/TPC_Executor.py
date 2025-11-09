from .Tick import Tick
from .Status import Status
from .Task import TaskType

class TPC_Executor(Tick):
    def __init__(self, task_type):
        super().__init__()
        self.task_type = task_type
        self.active_task = None

        self.STATUS_MAP = {
            TaskType.VPU: Status.EXEC_VPU,
            TaskType.ME: Status.EXEC_ME,
            TaskType.FE: Status.EXEC_FE,
        }

    def add_task(self, task):
        self.active_task = task

    def _action(self):
        print(f'TPC_Executor {self.task_type.value}: action')
        match self.status:
            case Status.WAIT:
                self._wait()
            case Status.SEND_TO_EXECUTE:
                self._exec(self.active_task)
            case Status.EXEC_VPU:
                self._set_status(Status.WAIT)
            case Status.EXEC_ME:
                self._set_status(Status.WAIT)
            case Status.EXEC_FE:
                self._set_status(Status.WAIT)
            case _:
                print("Unknown Status")
                return None

    def _wait(self):
        print(f'TPC_Executor {self.task_type.value}: wait')
        if self.active_task:
            print(f'Start executing task {self.active_task.task_type}')
            if self.task_type != self.active_task.task_type:
                print(f'Wrong task type ({self.active_task.task_type})! This executor ({self.task_type}) cant work with that task type (({self.active_task.task_type}))')
            else:
                self._set_status(Status.SEND_TO_EXECUTE)

    def _exec(self, task):
        print(f'TPC_Executor {self.task_type.value}: exec')
        new_status = self.STATUS_MAP[self.task_type]
        if new_status is None:
            print(f"Unknown task type: {self.task_type}")
            return None
        self._set_status(new_status)

    def __str__(self):
        status = self.print_status()
        return f'TCP_Executor {self.task_type.value}: {status}'