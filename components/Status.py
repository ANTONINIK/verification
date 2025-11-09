from enum import Enum


class Status(Enum):
    WAIT = 0
    COLLECT_TO_LOCAL = 1
    SEND_TO_GLOBAL = 2
    EXEC_VPU = 4
    EXEC_ME = 5
    EXEC_FE = 6
