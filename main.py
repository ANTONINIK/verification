from components.TPC import TPC
from components.Task import TaskType, Task
from components.GlobalWorker import GlobalWorker

tpc_dict = {
    'tpc1': TPC(),
    'tpc2': TPC(),
    'tpc3': TPC(),
    'tpc4': TPC(),
    'tpc5': TPC(),
    'tpc6': TPC(),
    'tpc7': TPC(),
    'tpc8': TPC(),
}

tasks = [
    Task(0, 9, TaskType.VPU),
    Task(10, 19, TaskType.ME),
]

gw = GlobalWorker(tasks, tpc_dict)

ticks = 1000

for t in range(ticks):
    gw.tick()
    for tpc_name, tpc in tpc_dict.items():
        tpc.tick()
