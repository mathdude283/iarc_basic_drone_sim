from random import *

class Grid:
    """A class representing the grid of mines and safe locations"""
    def __init__(self, length: int, width: int, mine_density: float = 0.2):
        self.length = length
        self.width = width
        self.mine_density = mine_density
        self.grid = [['O' for _ in range(width)] for _ in range(length)]
        self.generate_grid()

    def get_length(self) -> int:
        # Get the length of the grid
        return self.length
    
    def get_width(self) -> int:
        # Get the width of the grid
        return self.width
    
    def get_grid(self) -> list[list[str]]:
        # Get the grid
        return self.grid

    def generate_grid(self):
        # Randomly place mines in the grid based on the mine density
        for i in range(self.length):
            for j in range(self.width):
                if random() < self.mine_density:
                    self.grid[i][j] = 'X'

    def print_grid(self):
        # Print the grid to the console
        for row in self.grid:
            print(" ".join(row))
        print()
    
    def check_valid_loc(self, loc: tuple[int, int]) -> bool:
        # Check if the location is within bounds and not a mine
        if 0 <= loc[0] < self.length and 0 <= loc[1] < self.width:
            return True
        return False
    
    def mine_at_loc(self, loc: tuple[int, int]) -> bool:
        # Check if the location is within bounds and contains a mine
        if self.check_valid_loc(loc):
            return self.grid[loc[0]][loc[1]] == 'X'
        print("Invalid location:", loc)
        return False

    def find_start_loc(self) -> int:
        # Find a valid starting location in the first row of the grid
        row_length = len(self.grid[0])
        row_middle = row_length // 2
        row_pos = row_middle
        direction = 1
        while self.grid[0][row_pos] == 'X':
            if direction == 1 and row_pos == row_length - 1:
                direction = -1
                row_pos = row_middle
            row_pos += direction
            if row_pos < 0:
                print("No valid starting locations found.")
                return None
        return row_pos
    