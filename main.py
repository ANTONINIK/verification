from components import CommandExecutor, Task, TaskType


def main():
    print("Start program")

    executor = CommandExecutor(tpc_count=1)

    tasks = [
        Task(0, 9, TaskType.VPU),
        Task(10, 19, TaskType.ME),
        Task(5, 14, TaskType.FE),
    ]

    print("\nInitial tasks:")
    for t in tasks:
        print(t)

    executor.execute(tasks)

    executor.print_summary()

    print("End program")


if __name__ == "__main__":
    import sys

    try:
        import pytest
    except Exception:
        print(
            "pytest is required to run tests before starting. Install it with: python -m pip install pytest"
        )
        sys.exit(1)

    rc = pytest.main(["-q", "TestCommandExecutor.py"])
    if rc != 0:
        print(f"Tests failed (exit code={rc}). Aborting run.")
        sys.exit(rc)

    main()
