from enum import Enum


class Status(Enum):
    WAIT = 0
    COLLECT_TO_LOCAL = 1
    SEND_TO_GLOBAL = 2
    EXEC_VPU = 3
    EXEC_ME = 4
    EXEC_FE = 5
