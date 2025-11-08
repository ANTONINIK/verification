from .Tick import Tick
from .TPC_Executor import TPC_Executor
from .TPC_CU import TPC_CU
from .Task import TaskType, Task

class TPC(Tick):
    def __init__(self, name:str='TPC_0'):
        super().__init__()
        self.name = name
        self.addr_start = None
        self.addr_end = None
        self.VPU_executor = TPC_Executor(task_type=TaskType.VPU)
        self.ME_executor = TPC_Executor(task_type=TaskType.ME)
        self.FE_executor = TPC_Executor(task_type=TaskType.FE)
        self.TPC_cu = TPC_CU(
            self.VPU_executor,
            self.ME_executor,
            self.FE_executor,
            self.addr_start,
            self.addr_end
        )

    def add_task(self, task:Task):
        self.TPC_cu.add_task(task)

    def _action(self):
        print(f'{self.name}: action')
        self.TPC_cu.tick()
        self.ME_executor.tick()
        self.FE_executor.tick()
        self.VPU_executor.tick()

    def __str__(self):
        status = self.print_status()
        return f'{self.name}: {status}'
