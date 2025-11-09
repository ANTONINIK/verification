from components.TPC import TPC
from components.Task import Task
from components.TaskType import TaskType
from components.GlobalWorker import GlobalWorker
from components.Unit import Unit
from typing import List


def main():
    print("Start program")

    TICK_COUNT = 5

    tasks = [
        Task(0, 9, TaskType.VPU),
        Task(10, 19, TaskType.ME),
        Task(5, 14, TaskType.FE),
    ]

    tpcs = [
        TPC(name="TPC_1"),
        # TPC(name='TPC_2'),
        # TPC(name='TPC_3'),
        # TPC(name='TPC_4'),
        # TPC(name='TPC_5'),
        # TPC(name='TPC_6'),
        # TPC(name='TPC_7'),
        # TPC(name='TPC_8'),
    ]

    gw = GlobalWorker("GlobalWorker", tasks, tpcs)

    units: List[Unit] = [gw, *tpcs]

    for t in range(TICK_COUNT):
        print(f"Tick: {t}")
        for u in units:
            u.tick()
            print(u)

    print("End program")


if __name__ == "__main__":
    main()
