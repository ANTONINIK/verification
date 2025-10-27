from Tick import Tick
from TPC_Executor import TPC_Executor
from TPC_CU import TPC_CU
from Task import TaskType, Task

class TPC(Tick):
    def __init__(self):
        super().__init__()
        self.VPU_executor = TPC_Executor(task_type=TaskType.VPU)
        self.ME_executor = TPC_Executor(task_type=TaskType.ME)
        self.FE_executor = TPC_Executor(task_type=TaskType.FE)
        self.TPC_cu = TPC_CU(
            self.VPU_executor,
            self.ME_executor,
            self.FE_executor
        )

    def add_task(self, task:Task):
        self.TPC_cu.add_task(task)

    def _action(self):
        self.TPC_cu.tick()
        self.ME_executor.tick()
        self.FE_executor.tick()
        self.VPU_executor.tick()