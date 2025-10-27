from enum import Enum

class Status(Enum):
    WAIT = 0
    ACC_TO_GLOBAL = 500
    ACC_TO_LOCAL = 500
    EXEC_VPU = 4
    EXEC_ME = 256
    EXEC_FE = 1