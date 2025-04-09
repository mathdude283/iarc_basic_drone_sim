import math


from grid import Grid
from drone_state import DroneState

class Drone:
    """A class representing a drone that can move around the grid"""
    def __init__(self, pos: tuple[int, int], grid: Grid):
        self.pos = pos
        self.grid = grid
        self.speed = 1
        self.distance_rem = 0
        self.scan_len = 2
        self.scan_rem = 0
        self.task_list = []
        self.state = DroneState.IDLE
        self.scan_target = False

    
    def distance(self, target: tuple[int, int]) -> float:
        # Calculate the Euclidean distance to the target location
        return round(math.sqrt((self.pos[0] - target[0]) ** 2 + (self.pos[1] - target[1]) ** 2), 1)
    
    def distance(self, start: tuple[int, int], target: tuple[int, int]) -> float:
        # Calculate the Euclidean distance between two points
        return round(math.sqrt((start[0] - target[0]) ** 2 + (start[1] - target[1]) ** 2), 1)

    def start_move(self):
        # Starts the drone moving towards the target location
        self.state = DroneState.MOVING
        self.target = self.task_list[0][0]
        self.moving = True
        self.distance_rem = self.distance(self.task_list[0])
        self.scan_target = self.task_list[0][1]

    def move_for_time(self, time: float):
        # Move the drone for a specified time
        self.distance_rem -= time * self.speed
        if self.distance_rem <= 0:
            self.pos = self.target
            self.distance_rem = 0
    
    def finish_move(self):
        self.task_list.pop(0)
        if self.scan_target:
            self.start_scan()
        elif len(self.task_list) > 0:
            self.start_move()
        else:
            self.state = DroneState.IDLE

    def start_scan(self) -> bool:
        # Starts scanning for a mine at the specified location
        self.state = DroneState.SCANNING
        self.scan_rem = self.scan_len

    def scan_for_time(self, time: float):
        # Scan the area for a specified time
        self.scan_rem -= time
        if self.scan_rem <= 0:
            self.scan_rem = 0
    
    def finish_scan(self) -> tuple[bool, tuple[int, int]]:
        # Check if the current position contains a mine
        if len(self.task_list) > 0:
            self.start_move()
        else: self.state = DroneState.IDLE

        return (self.grid.mine_at_loc(self.pos), self.pos)
    
    def get_state(self) -> DroneState:
        # Check if the drone is currently moving
        return self.state

    def get_speed(self) -> int:
        # Get the speed of the drone
        return self.speed
    
    def get_read_delay(self) -> int:
        # Get the read delay of the drone
        return self.scan_len
    
    def get_task_list(self) -> list[tuple[tuple[int, int], bool]]:
        # Get the list of tasks assigned to the drone
        return self.task_list
    
    def run_frame(self, time: float):
        # Run a frame of the drone's operation
        frame_return = None
        if self.state == DroneState.IDLE and len(self.task_list) > 0:
            self.start_move()
        if self.state == DroneState.MOVING:
            self.move_for_time(time)
            if self.distance_rem == 0:
                self.finish_move()
        elif self.state == DroneState.SCANNING:
            self.scan_for_time(time)
            if self.scan_rem == 0:
                frame_return = self.finish_scan()
        return frame_return

    def tasks_estimate(self) -> float:
        # Estimate the time required to complete the tasks
        time_estimate = 0
        if self.state == DroneState.SCANNING:
            time_estimate += self.scan_rem
        elif self.state == DroneState.MOVING:
            time_estimate += self.distance_rem / self.speed
        if self.state != DroneState.MOVING:
            time_estimate += self.distance(self.pos, self.task_list[0][0]) / self.speed
            if self.task_list[0][1]:
                time_estimate += self.scan_len
        for task in range(1,len(self.task_list)):
            task_distance = self.distance(self.task_list[task - 1][0], self.task_list[task][0])
            time_estimate += task_distance / self.speed
            if self.task_list[task][1]:
                time_estimate += self.scan_len
        return time_estimate


class DroneController(Drone):
    """A class representing the controller drone"""
    def __init__(self, pos: tuple[int, int], grid: Grid, drones: list[Drone, Drone, Drone]):
        super().__init__(pos, grid)
        self.drones = drones
    
    def assign_drone(self, target: tuple[int, int]):
        pass