from .Unit import Unit
from .Memory import Memory
from typing import TYPE_CHECKING, List, Tuple, Optional
from .BColors import BColors
if TYPE_CHECKING:
    from .Task import Task
    from .TPC import TPC


class GlobalWorker(Unit):
    def __init__(self, name: str, tasks: List["Task"], tpcs: List["TPC"]):
        super().__init__(name, BColors.OKBLUE, 1)
        self._queue: List["Task"] = tasks
        self._tpcs: List["TPC"] = tpcs
        self.completed_tasks: List["Task"] = []
        self.hbm: List[Tuple[int, int, "TPC"]] = []

    def _action(self):
        self.log(f"Queue length: {len(self._queue)}")

        if not self._queue:
            return

        candidate_task = self._queue[0]

        # 1. Проверяем, есть ли уже TPC, которому принадлежит диапазон HBM
        assigned_tpc = self._find_tpc_by_hbm_range(candidate_task)

        self.log(f"Assigned TPC from HBM range: {assigned_tpc}")

        # 2. Если нет, ищем наименее загруженный TPC
        if assigned_tpc is None:
            for tpc in sorted(self._tpcs, key=lambda t: t.get_total_task_count()):
                if not Memory.check_conflict(self.hbm, candidate_task.addr_start, candidate_task.addr_end, tpc):
                    assigned_tpc = tpc
                    break

            if assigned_tpc is None:
                self.log("All TPCs are busy or memory ranges conflict, waiting...")
                return

        # 3. Резервируем диапазон памяти
        self.log(f"Assigning {candidate_task} to {assigned_tpc.name}")
        Memory.allocate(self.hbm, candidate_task.addr_start, candidate_task.addr_end, assigned_tpc)

        # 4. Назначаем задачу TPC
        assigned_tpc.add_task(self._queue.pop(0), self._on_complete_task)

    def _on_complete_task(self, task: "Task"):
        self.log(f"{task} completed and collected")
        self.completed_tasks.append(task)

    def _select_least_loaded_tpc(self) -> "TPC":
        return min(self._tpcs, key=lambda t: t.get_total_task_count())
    
    def _find_tpc_by_hbm_range(self, task: "Task") -> Optional["TPC"]:
        for s, e, tpc in self.hbm:
            if task.addr_start >= s and task.addr_end <= e:
                return tpc
        return None

        