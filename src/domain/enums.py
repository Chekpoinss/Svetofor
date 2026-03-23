from enum import Enum, auto

class LightColor(Enum):
    RED = auto()
    GREEN = auto()
    NONE = auto()

class ActionSignal(Enum):
    STOP = auto()
    GO = auto()
    NONE = auto()