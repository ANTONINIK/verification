import pytest
from components import CommandExecutor, Task, TaskType


class TestCommandExecutorBasic:
    
    def test_single_task_execution(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [Task(0, 9, TaskType.VPU)]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 1
        assert completed_tasks[0].is_completed
        assert ticks_used > 0
    
    def test_multiple_tasks_execution(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(5, 14, TaskType.FE),
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 3
        assert all(task.is_completed for task in completed_tasks)
        assert ticks_used > 0
    
    def test_different_task_types(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 3
        task_types = {task.task_type for task in completed_tasks}
        assert TaskType.VPU in task_types
        assert TaskType.ME in task_types
        assert TaskType.FE in task_types


class TestCommandExecutorMultipleTPC:
    
    def test_multiple_tpcs_execution(self):
        executor = CommandExecutor(tpc_count=2)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 3
        assert all(task.is_completed for task in completed_tasks)
    
    def test_four_tpcs_execution(self):
        executor = CommandExecutor(tpc_count=4)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
            Task(30, 39, TaskType.VPU),
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 4
        assert all(task.is_completed for task in completed_tasks)


class TestCommandExecutorMemory:
    
    def test_non_overlapping_memory_ranges(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 2
    
    def test_overlapping_memory_ranges_same_owner(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [
            Task(0, 15, TaskType.VPU),
            Task(10, 20, TaskType.ME),
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 2
    
    def test_get_memory_ranges(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [Task(0, 9, TaskType.VPU)]
        
        executor.execute(tasks)
        memory_ranges = executor.get_memory_ranges()
        
        assert isinstance(memory_ranges, list)


class TestCommandExecutorReset:
    
    def test_reset_between_executions(self):
        executor = CommandExecutor(tpc_count=1)
        
        tasks1 = [Task(0, 9, TaskType.VPU)]
        completed1, ticks1 = executor.execute(tasks1)
        
        tasks2 = [Task(10, 19, TaskType.ME)]
        completed2, ticks2 = executor.execute(tasks2)
        
        assert len(completed1) == 1
        assert len(completed2) == 1
        assert completed1[0].id != completed2[0].id
    
    def test_completed_tasks_cleared_after_reset(self):
        executor = CommandExecutor(tpc_count=1)
        
        tasks1 = [Task(0, 9, TaskType.VPU)]
        executor.execute(tasks1)
        assert len(executor.global_worker.completed_tasks) == 1
        
        tasks2 = [Task(10, 19, TaskType.ME)]
        executor.execute(tasks2)
        assert len(executor.global_worker.completed_tasks) == 1


class TestCommandExecutorEdgeCases:
    
    def test_empty_task_list(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = []
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 0
        assert ticks_used == 0
    
    def test_large_number_of_tasks(self):
        executor = CommandExecutor(tpc_count=2)
        tasks = [
            Task(i * 10, i * 10 + 9, TaskType.VPU if i % 3 == 0 else (TaskType.ME if i % 3 == 1 else TaskType.FE))
            for i in range(10)
        ]
        
        completed_tasks, ticks_used = executor.execute(tasks)
        
        assert len(completed_tasks) == 10
        assert all(task.is_completed for task in completed_tasks)
    
    def test_maximum_ticks_exceeded(self):
        executor = CommandExecutor(tpc_count=1, max_ticks=5)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        
        with pytest.raises(RuntimeError):
            executor.execute(tasks)


class TestCommandExecutorTaskProperties:
    
    def test_task_ids_unique(self):
        executor = CommandExecutor(tpc_count=1)
        tasks1 = [Task(0, 9, TaskType.VPU)]
        completed1, _ = executor.execute(tasks1)
        
        executor2 = CommandExecutor(tpc_count=1)
        tasks2 = [Task(0, 9, TaskType.VPU)]
        completed2, _ = executor2.execute(tasks2)
        
        assert completed1[0].id != completed2[0].id
    
    def test_task_properties_preserved(self):
        executor = CommandExecutor(tpc_count=1)
        original_task = Task(5, 15, TaskType.ME)
        tasks = [original_task]
        
        completed_tasks, _ = executor.execute(tasks)
        
        completed_task = completed_tasks[0]
        assert completed_task.addr_start == original_task.addr_start
        assert completed_task.addr_end == original_task.addr_end
        assert completed_task.task_type == original_task.task_type


class TestCommandExecutorTicks:
    
    def test_ticks_increase_with_task_complexity(self):
        executor1 = CommandExecutor(tpc_count=1)
        tasks1 = [Task(0, 9, TaskType.VPU)]
        _, ticks1 = executor1.execute(tasks1)
        
        executor2 = CommandExecutor(tpc_count=1)
        tasks2 = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        _, ticks2 = executor2.execute(tasks2)
        
        assert ticks2 > ticks1
    
    def test_more_tpcs_reduces_ticks(self):
        executor1 = CommandExecutor(tpc_count=1)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        _, ticks1 = executor1.execute(tasks)
        
        executor2 = CommandExecutor(tpc_count=3)
        _, ticks2 = executor2.execute(tasks)
        
        assert ticks2 <= ticks1


class TestTaskTiming:
    
    def test_start_time_is_set(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [Task(0, 9, TaskType.VPU)]
        
        completed_tasks, _ = executor.execute(tasks)
        
        assert completed_tasks[0].start_time == 0
    
    def test_end_time_is_set(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [Task(0, 9, TaskType.VPU)]
        
        completed_tasks, _ = executor.execute(tasks)
        
        assert completed_tasks[0].end_time is not None
        assert completed_tasks[0].end_time > 0
    
    def test_latency_is_calculated(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [Task(0, 9, TaskType.VPU)]
        
        completed_tasks, ticks = executor.execute(tasks)
        
        assert completed_tasks[0].latency is not None
        assert completed_tasks[0].latency == ticks
    
    def test_latency_increases_with_multiple_tasks(self):
        executor1 = CommandExecutor(tpc_count=1)
        tasks1 = [Task(0, 9, TaskType.VPU)]
        completed1, _ = executor1.execute(tasks1)
        latency1 = completed1[0].latency
        
        executor2 = CommandExecutor(tpc_count=1)
        tasks2 = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        completed2, _ = executor2.execute(tasks2)
        latency_last = completed2[-1].latency
        
        assert latency_last > latency1
    
    def test_all_tasks_have_latency(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        
        completed_tasks, _ = executor.execute(tasks)
        
        assert all(task.latency is not None for task in completed_tasks)
        assert all(task.latency > 0 for task in completed_tasks)
    
    def test_latency_formula(self):
        executor = CommandExecutor(tpc_count=1)
        tasks = [Task(0, 9, TaskType.VPU)]
        
        completed_tasks, _ = executor.execute(tasks)
        task = completed_tasks[0]
        
        assert task.latency == task.end_time - task.start_time
    
    def test_different_task_types_different_latency(self):
        executor = CommandExecutor(tpc_count=3)
        tasks = [
            Task(0, 9, TaskType.VPU),
            Task(10, 19, TaskType.ME),
            Task(20, 29, TaskType.FE),
        ]
        
        completed_tasks, _ = executor.execute(tasks)
        
        latencies = [task.latency for task in completed_tasks]
        assert len(set(latencies)) >= 1
    
    def test_task_without_completion_no_end_time(self):
        executor = CommandExecutor(tpc_count=1)
        task = Task(0, 9, TaskType.VPU)
        
        assert task.end_time is None
        assert task.latency is None
    
    def test_task_with_only_start_time_no_latency(self):
        executor = CommandExecutor(tpc_count=1)
        task = Task(0, 9, TaskType.VPU)
        task.start_time = 5
        
        assert task.latency is None
        assert task.end_time is None


    class TestTaskExecutedBy:

        def test_executed_by_set_single_task(self):
            executor = CommandExecutor(tpc_count=1)
            tasks = [Task(0, 9, TaskType.VPU)]

            completed_tasks, _ = executor.execute(tasks)

            assert completed_tasks[0].executed_by is not None
            assert 'Executor' in completed_tasks[0].executed_by

        def test_executed_by_set_all_tasks(self):
            executor = CommandExecutor(tpc_count=2)
            tasks = [
                Task(0, 9, TaskType.VPU),
                Task(10, 19, TaskType.ME),
                Task(20, 29, TaskType.FE),
            ]

            completed_tasks, _ = executor.execute(tasks)

            assert all(t.executed_by is not None for t in completed_tasks)
            assert all('Executor' in t.executed_by for t in completed_tasks)
