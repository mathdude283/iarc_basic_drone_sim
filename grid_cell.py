from cell_mine_state import CellMineState

class GridCell:
    """
    Class representing a cell in the grid.
    """
    def __init__(self, mine_state: CellMineState = CellMineState.SAFE) -> None:
        if (mine_state == CellMineState.UNKNOWN or mine_state == CellMineState.QUEUED or mine_state == CellMineState.SCANNING):
            raise ValueError("Grid mine state cannot be UNKNOWN, QUEUED, or SCANNING.")
        self.mine_state: CellMineState = mine_state

    def set_mine_state(self, mine_state: CellMineState) -> None:
        """Sets the mine state of the cell."""
        if (mine_state == CellMineState.UNKNOWN or mine_state == CellMineState.QUEUED or mine_state == CellMineState.SCANNING):
            raise ValueError("Grid mine state cannot be UNKNOWN, QUEUED, or SCANNING.")
        self.mine_state = mine_state
    
    def get_mine_state(self) -> CellMineState:
        """Returns the mine state of the cell."""
        return self.mine_state
    
    def __str__(self) -> str:
        """Returns a string representation of the cell."""
        if self.mine_state == CellMineState.EMPTY:
            return "O"
        elif self.mine_state == CellMineState.MINE:
            return "X"
        else:
            raise ValueError(f"Unknown mine state: {self.mine_state}")