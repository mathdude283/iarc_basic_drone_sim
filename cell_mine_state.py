from enum import Enum

class CellMineState(Enum):
    """Enum representing whether a cell contains a mine."""
    UNKNOWN = 0
    EMPTY = 1
    MINE = 2
    QUEUED = 3
    SCANNING = 4