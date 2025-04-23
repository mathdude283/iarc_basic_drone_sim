from random import *

from cell_mine_state import CellMineState
from grid_cell import GridCell

class Grid:
    
    """
    Class representing whether each cell has a mine.
    """
    def __init__(self, length: int = 10, width: int = 10, mine_density: float = 0.2, cell_size: float = 1) -> None:
        if length <= 0:
            raise ValueError("Length must be positive integer.")
        if width < 4:
            raise ValueError("Width must be at least 4.")
        if mine_density < 0 or mine_density > 1:
            raise ValueError("Mine density must be between 0 and 1, inclusive.")
        if cell_size <= 0:
            raise ValueError("Cell size must be positive integer.")
        self.length: int = length
        self.width: int = width
        self.mine_density: float = mine_density
        self.cell_size: float = cell_size
    