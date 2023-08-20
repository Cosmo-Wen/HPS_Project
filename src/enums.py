from enum import Enum, auto

class Instructions(Enum):
    START = auto()
    END = auto()
    MOVE = auto()
    RETURN = auto()
    INVALID = auto()
    LOG = auto()

class States(Enum):
    IDLE = auto()
    ONLINE = auto()
    INVALID = auto()

class Actions(Enum):
    NOTHING = auto()
    HALT = auto()
    INVALID = auto()