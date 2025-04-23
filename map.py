from cell_mine_state import CellMineState
from cell_safety_state import CellSafetyState
from map_cell import MapCell

class Map:
    
    """
    Class representing known mine locations and safety states of cells in a minefield.
    """
    def __init__(self, length: int = 10, width: int = 10, cell_size: float = 1) -> None:
        if length <= 0:
            raise ValueError("Length must be positive integer.")
        if width < 4:
            raise ValueError("Width must be at least 4.")
        if cell_size <= 0:
            raise ValueError("Cell size must be positive integer.")
        self.length: int = length
        self.width: int = width
        self.cell_size: float = cell_size