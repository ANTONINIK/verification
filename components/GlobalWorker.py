from .Unit import Unit
from .Memory import Memory
from typing import TYPE_CHECKING, List, Tuple, Optional
if TYPE_CHECKING:
    from .Task import Task
    from .TPC import TPC


class GlobalWorker(Unit):
    def __init__(self, name: str, tasks: List["Task"], tpcs: List["TPC"]):
        super().__init__(name)
        self._queue: List["Task"] = tasks
        self.completed_tasks: List["Task"] = []
        self._tpcs: List["TPC"] = tpcs
        self._hbm: List[Tuple[int, int, "TPC"]] = []

    def _action(self):
        if not self._queue:
            return

        candidate = self._queue[0]

        # 1. Проверяем, есть ли уже TPC, которому принадлежит диапазон HBM
        assigned_tpc = self._find_tpc_by_hbm_range(candidate)

        # 2. Если нет, ищем наименее загруженный TPC
        if assigned_tpc is None:
            assigned_tpc = self._select_least_loaded_tpc()

        # 3. Резервируем диапазон памяти
        Memory.allocate(self._hbm, candidate.addr_start, candidate.addr_end, assigned_tpc)

        # 4. Назначаем задачу TPC
        assigned_tpc.add_task(self._queue.pop(0), self._on_complete_task)

    def _on_complete_task(self, task: "Task"):
        self.completed_tasks.append(task)

    def _select_least_loaded_tpc(self) -> "TPC":
        return min(self._tpcs, key=lambda t: t.get_total_task_count())
    
    def _find_tpc_by_hbm_range(self, task: "Task") -> Optional["TPC"]:
        for s, e, tpc in self._hbm:
            if Memory._ranges_overlap(task.addr_start, task.addr_end, s, e):
                return tpc
        return None

        