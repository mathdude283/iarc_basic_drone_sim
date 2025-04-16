from enum import Enum

class TileState(Enum):
    """Enum representing the state of a tile."""
    UNKNOWN = 0
    SAFE = 1
    UNSAFE = 2
    MINE = 3
    QUEUED = 4
    SCANNING = 5