import math

from grid import Grid

class Drone:
    """A class representing a drone that can move around the grid"""
    def __init__(self, pos: tuple[int, int], grid: Grid):
        self.pos = pos
        self.grid = grid
        self.speed = 1
        self.target = self.pos
        self.moving = False
        self.distance_rem = 0
    
    def distance(self, target: tuple[int, int]) -> float:
        # Calculate the Euclidean distance to the target location
        return round(math.sqrt((self.pos[0] - target[0]) ** 2 + (self.pos[1] - target[1]) ** 2), 1)
    
    def check_square(self, loc) -> bool:
        # Check if the location is within bounds and contains a mine
        return self.grid.mine_at_loc(loc)
    
    def move(self, target: tuple[int, int]):
        # Starts the drone moving towards the target location
        if not self.grid.check_valid_loc(target):
            print("Invalid target location:", target)
            return
        self.target = target
        self.moving = True
        self.distance_rem = self.distance(target)
    
    def check_moving(self) -> bool:
        # Check if the drone is currently moving
        return self.moving
    
    def move_time(self, time: float):
        # Move the drone for a specified time
        if self.moving:
            self.distance_rem -= time * self.speed
            if self.distance_rem <= 0:
                self.pos = self.target
                self.moving = False
                self.distance_rem = 0                

class DroneController(Drone):
    """A class representing the controller drone"""
    def __init__(self, pos: tuple[int, int], grid: Grid, drones: list[Drone, Drone, Drone]):
        super().__init__(pos, grid)
        self.drones = drones
    
    
    