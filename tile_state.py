from enum import Enum

# Considering changing to one map of cell safety and another of mine locations

class TileState(Enum):
    """Enum representing the state of a tile."""
    UNKNOWN = 0
    SAFE = 1
    UNSAFE = 2
    UNSAFE_UNKNOWN = 3
    MINE = 4
    QUEUED = 5
    UNSAFE_QUEUED = 6
    SCANNING = 7
    UNSAFE_SCANNING = 8