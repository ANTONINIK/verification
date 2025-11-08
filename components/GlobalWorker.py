from .Tick import Tick

class GlobalWorker(Tick):
    def __init__(self, tasks, tpcs):
        super().__init__()
        self.queue = tasks
        self.tpcs = tpcs

    def _action(self):
        print('GlobalWorker: action')
        if len(self.queue) > 0:
            task_to_execute = self.queue.pop(0)
            tpc = self._find_tpc_for_task(task_to_execute)
            if tpc:
                print(f'{task_to_execute} ---> {tpc}')
                tpc.add_task(task_to_execute)
            else:
                print(f'{task_to_execute} ---> end of que')
                self.queue.append(task_to_execute)  # добавляем в конец очереди, если не нашелся tpc

    def _find_tpc_for_task(self, task_to_execute):
        print('GlobalWorker: find_tpc_for_task')
        suitable_tpc = None
        for tpc in self.tpcs:
            if tpc.addr_start is not None:
                if ((task_to_execute.addr_start >= tpc.addr_start) |
                        (task_to_execute.addr_start <= tpc.addr_end) |
                        (task_to_execute.addr_end >= tpc.addr_start) |
                        (task_to_execute.addr_end <= tpc.addr_end)):
                    suitable_tpc = tpc
                    return suitable_tpc
            elif suitable_tpc is None:
                suitable_tpc = tpc
        return suitable_tpc

    def __str__(self):
        status = self.print_status()
        return f'GlobalWorker: {status}'