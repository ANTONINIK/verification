from Tick import Tick

class GlobalWorker(Tick):
    def __init__(self, tasks, tpcs):
        super().__init__()
        self.queue = tasks
        self.tpc_dict = tpcs

    def _action(self):
        if len(self.queue) > 0:
            task_to_execute = self.queue[0]
            tpc = self._find_tpc_for_task(task_to_execute)
            if tpc:
                tpc.add_task(task_to_execute)
                a.pop(0)

    def _find_tpc_for_task(self, task_to_execute):
        suitable_tpc = None
        for tpc_name, tpc in self.tpc_dict.items():
            if tpc.addr_start is not None:
                if ((task_to_execute.addr_start >= tpc.addr_start) |
                        (task_to_execute.addr_start <= tpc.addr_end) |
                        (task_to_execute.addr_end >= tpc.addr_start) |
                        (task_to_execute.addr_end <= tpc.addr_end)):
                    suitable_tpc = tpc
                    return suitable_tpc
            else:
                suitable_tpc = tpc
        return suitable_tpc