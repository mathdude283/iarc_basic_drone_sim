from cell_mine_state import CellMineState
from cell_safety_state import CellSafetyState

class MapCell:
    """
    Class representing a cell in the map.
    """
    def __init__(self, mine_state: CellMineState = CellMineState.UNKNOWN, safety_state: CellSafetyState = CellSafetyState.UNKNOWN) -> None:
        self.mine_state: CellMineState = mine_state
        self.safety_state: CellSafetyState = safety_state

    def set_mine_state(self, mine_state: CellMineState) -> None:
        """Sets the mine state of the cell.
        If the mine state is MINE, the safety state is set to UNSAFE.
        """
        self.mine_state = mine_state
        if self.mine_state == CellMineState.MINE:
            self.safety_state = CellSafetyState.UNSAFE

    def set_safety_state(self, safety_state: CellSafetyState) -> None:
        """Sets the safety state of the cell.
        Set the mine state before setting this state.
        Will raise an error if safety_state is incompatiple with self.mine_state"""
        if (((safety_state == CellSafetyState.SAFE or safety_state == CellSafetyState.UNKNOWN) and self.mine_state == CellMineState.MINE)
            or (safety_state == CellSafetyState.SAFE and (self.mine_state == CellMineState.UNKNOWN or self.mine_state == CellMineState.QUEUED or self.mine_state == CellMineState.SCANNING))):
            raise ValueError(f"Safety state {safety_state} is incompatible with mine state {self.mine_state}.")
        self.safety_state = safety_state
    
    def get_mine_state(self) -> CellMineState:
        """Returns the mine state of the cell."""
        return self.mine_state
    
    def get_safety_state(self) -> CellSafetyState:
        """Returns the safety state of the cell."""
        return self.safety_state
    
    def __str__(self) -> str:
        """Returns a string representation of the cell."""
        if (self.safety_state == CellSafetyState.UNSAFE and self.mine_state == CellMineState.MINE):
            return "X"
        elif (self.safety_state == CellSafetyState.UNSAFE and self.mine_state == CellMineState.EMPTY):
            return "!"
        elif (self.safety_state == CellSafetyState.UNSAFE and (self.mine_state == CellMineState.UNKNOWN or self.mine_state == CellMineState.QUEUED or self.mine_state == CellMineState.SCANNING)):
            return "~"
        elif (self.safety_state == CellSafetyState.SAFE and self.mine_state == CellMineState.EMPTY):
            return "O"
        elif ((self.safety_state == CellSafetyState.UNKNOWN) and (self.mine_state == CellMineState.UNKNOWN or self.mine_state == CellMineState.QUEUED or self.mine_state == CellMineState.SCANNING or self.mine_state == CellMineState.EMPTY)):
            return "?"
        else:
            raise ValueError(f"Unknown cell state comination: {self.safety_state}, {self.mine_state}")