from enum import Enum

class DroneState(Enum):
    """Enum representing the state of the drone."""
    IDLE = 0
    MOVING = 1
    SCANNING = 2