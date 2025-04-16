from enum import Enum

class TileState(Enum):
    """Enum representing the state of a tile."""
    UNKNOWN = 0
    SAFE = 1
    MINE = 2
    QUEUED = 3
    SCANNING = 4