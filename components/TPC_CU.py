from Tick import Tick
from Status import Status
from Task import TaskType, Task

class TPC_CU(Tick):
    def __init__(self, VPU_executor, ME_executor, FE_executor):
        super().__init__()
        self.queue = []
        self.active_task = None
        self.VPU_executor = VPU_executor
        self.ME_executor = ME_executor
        self.FE_executor = FE_executor

    def _wait(self):
        print(self.status.value)
        if self.active_task is None:
            if len(self.queue) > 0:
                self.active_task = self.queue[0]
                self.queue.pop(0)
                self._set_status(Status.COLLECT)
            # else:
            #     len(self.queue) = 0:
            #     if self.addr_start is None:

    def _collect(self):
        print(self.status.value)
        if self.addr_start is None:
            self.addr_start = self.active_task.addr_start
            self.addr_end = self.active_task.addr_end
        else:
            pass

    def _action(self):
        match self.status:
            case Status.WAIT:
                self._wait()
            case Status.COLLECT:
                self._collect()
            case Status.SEND:
                print(self.status.value)
            case Status.EXEC:
                print(self.status.value)

            case _:
                print("Unknown Status")

    def _vpu(self, task:Task):
        pass

    def _me(self, task:Task):
        pass

    def _fe(self, task:Task):
        pass

    def _send_to_global(self):
        self.addr_start = None
        self.addr_end = None

    def _get_from_global(self, task:Task):
        self.addr_start = task.addr_start
        self.addr_end = task.addr_end

    def add_task(self, task:Task):
        self.queue.append(task)