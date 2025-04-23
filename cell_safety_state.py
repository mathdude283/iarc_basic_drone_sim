from enum import Enum

class CellSafetyState(Enum):
    """Enum representing the safety state of a cell in a minefield."""
    UNKNOWN = 0  # The safety state of the cell is unknown.
    SAFE = 1  # The cell is known to be safe.
    UNSAFE = 2  # The cell is known to be unsafe.