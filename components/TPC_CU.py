from .Tick import Tick
from .Status import Status
from .Task import TaskType, Task

class TPC_CU(Tick):
    def __init__(self, VPU_executor, ME_executor, FE_executor, addr_start, addr_end):
        super().__init__()
        self.queue = []
        self.active_task = None
        self.addr_start = addr_start
        self.addr_end = addr_end
        self.executors = {
            TaskType.VPU: VPU_executor,
            TaskType.ME: ME_executor,
            TaskType.FE: FE_executor,
        }

    def _wait(self):
        print(f'TPC_CU: wait')
        if self.active_task is None:
            if len(self.queue) > 0:
                self.active_task = self.queue.pop(0)
                print('TPC_cu: Start collecting data to local memory')
                if self.addr_start is None:
                    self._set_status(Status.COLLECT_TO_LOCAL)
                    print('TPC_CU: Need to copy data in local memory')
                elif ((self.addr_start > self.active_task.addr_start) |
                    (self.addr_end < self.active_task.addr_end)):
                    self._set_status(Status.COLLECT_TO_LOCAL)
                    print('TPC_CU: Need to copy data in local memory')
                else:
                    self._set_status(self.active_task.status)
                    print('TPC_CU: Data already in local memory')
            else:
                if self.addr_start:
                    print('TPC_cu: Start sending data to global memory')
                    self._set_status(Status.SEND_TO_GLOBAL)

    def _action(self):
        print(f'TPC_CU: action')
        match self.status:
            case Status.WAIT:
                self._wait()
            case Status.COLLECT_TO_LOCAL:
                self._get_from_global(self.active_task)
            case Status.SEND_TO_GLOBAL:
                self._send_to_global()
            case Status.SEND_TO_EXECUTE:
                self._send_to_execute(self.active_task)
            case _:
                print("Unknown Status")
                return None

    def _send_to_execute(self, task: Task):
        print(f'TPC_CU: send_to_execute')
        executor = self.executors[task.task_type]
        if executor is None:
            print(f"Unknown task type: {task.task_type}")
            return None

        if executor.active_task is None:
            executor.add_task(task)
        else:
            self.queue.append(task)

        print(f'TPC_CU: {self.active_task} ---> {executor}')
        self.active_task = None
        self.status = Status.WAIT

    def _send_to_global(self):
        print(f'TPC_CU: send_to_global')
        self.addr_start = None
        self.addr_end = None
        self.status = Status.WAIT
        print('TPC_CU: Data sent to global memory')

    def _get_from_global(self, task:Task):
        print(f'TPC_CU: get_from_global')
        if self.addr_start is None:
            self.addr_start = self.active_task.addr_start
            self.addr_end = self.active_task.addr_end
        else:
            if self.addr_start > self.active_task.addr_start:
                self.addr_start = self.active_task.addr_start
            if self.addr_end < self.active_task.addr_end:
                self.addr_end = self.active_task.addr_end

        self._set_status(Status.SEND_TO_EXECUTE)
        print('TPC_CU: Data copied in local memory')

    def add_task(self, task:Task):
        self.queue.append(task)
        print(f'TPC_CU: {task} added to queue')

    def __str__(self):
        status = self.print_status()
        return f'TCP_cu: {status}'