from components.TPC import TPC
from components.Task import TaskType, Task
from components.GlobalWorker import GlobalWorker

tpcs = [
    TPC(name='TPC_1'),
    # TPC(name='TPC_2'),
    # TPC(name='TPC_3'),
    # TPC(name='TPC_4'),
    # TPC(name='TPC_5'),
    # TPC(name='TPC_6'),
    # TPC(name='TPC_7'),
    # TPC(name='TPC_8'),
]

tasks = [
    Task(0, 9, TaskType.VPU),
    # Task(10, 19, TaskType.ME),
    # Task(20, 29, TaskType.FE),
]

gw = GlobalWorker(tasks, tpcs)
ticks = 5

print('START PROGRAM')
print('initial params:')
print(gw)
for tpc in tpcs:
    print(tpc)
for task in tasks:
    print(task)

print('='*100)
print('START PROCESS')

for t in range(ticks):
    print(f'TICK: {t}')
    gw.tick()
    print(gw)
    print('*'*50)
    for tpc in tpcs:
        tpc.tick()
        print()
        print(tpc)
        print(tpc.TPC_cu)
        print(tpc.FE_executor)
        print(tpc.ME_executor)
        print(tpc.VPU_executor)
        print('*'*50)

    print('='*100)
