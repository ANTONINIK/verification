from enum import Enum


class Status(Enum):
    WAIT = 0
    COLLECT_TO_LOCAL = 2
    SEND_TO_GLOBAL = 2
    SEND_TO_EXECUTE = 1
    EXEC_VPU = 2
    EXEC_ME = 2
    EXEC_FE = 2