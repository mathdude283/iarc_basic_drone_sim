import math


from grid import Grid
from map import Map
from drone_state import DroneState
from tile_state import TileState

class Drone:
    """A class representing a drone that can move around the grid"""
    def __init__(self, pos: list[int, int], grid: Grid) -> None:
        self.pos: list[int, int] = pos
        self.grid: Grid = grid
        self.speed: float = 1
        self.distance_rem: float = 0
        self.scan_len: float = 2
        self.scan_rem: float = 0
        self.task_list: list[list[int, int], bool] = []
        self.state: DroneState = DroneState.IDLE
        self.scan_target: bool = False

    
    def distance(self, target: list[int, int]) -> float:
        # Calculate the Euclidean distance to the target location
        return round(math.sqrt((self.pos[0] - target[0]) ** 2 + (self.pos[1] - target[1]) ** 2), 1)
    
    def distance(self, start: list[int, int], target: list[int, int]) -> float:
        # Calculate the Euclidean distance between two points
        return round(math.sqrt((start[0] - target[0]) ** 2 + (start[1] - target[1]) ** 2), 1)
    
    def start_scan(self) -> bool:
        # Starts scanning for a mine at the specified location
        if self.pos[0] >= self.grid.get_length() or self.pos[0] < 0 or self.pos[1] >= self.grid.get_width() or self.pos[1] < 0:
            raise ValueError("Location out of bounds")

        self.state = DroneState.SCANNING
        self.scan_rem = self.scan_len

    def scan_for_time(self, time: float) -> None:
        # Scan the area for a specified time
        self.scan_rem -= time
        if self.scan_rem <= 0:
            self.scan_rem = 0

    def start_move(self) -> None:
        # Starts the drone moving towards the target location
        self.state = DroneState.MOVING
        self.target = self.task_list[0][0]
        self.distance_rem = self.distance(self.task_list[0])
        self.scan_target = self.task_list[0][1]

    def move_for_time(self, time: float) -> None:
        # Move the drone for a specified time
        self.distance_rem -= time * self.speed
        if self.distance_rem <= 0:
            self.pos = self.target
            self.distance_rem = 0
    
    def finish_move(self) -> None:
        self.task_list.pop(0)
        if self.scan_target:
            self.start_scan()
        elif len(self.task_list) > 0:
            self.start_move()
        else:
            self.state = DroneState.IDLE
    
    def finish_scan(self) -> list[bool, list[int, int]]:
        # Check if the current position contains a mine
        if len(self.task_list) > 0:
            self.start_move()
        else: self.state = DroneState.IDLE

        return [self.grid.mine_at_loc(self.pos), self.pos]
    
    def get_state(self) -> DroneState:
        # Check if the drone is currently moving
        return self.state
    
    def get_pos(self) -> list[int, int]:
        # Get the current position of the drone
        return self.pos

    def get_speed(self) -> int:
        # Get the speed of the drone
        return self.speed
    
    def get_read_delay(self) -> int:
        # Get the read delay of the drone
        return self.scan_len
    
    def get_task_list(self) -> list[list[list[int, int], bool]]:
        # Get the list of tasks assigned to the drone
        return self.task_list
    
    def run_frame(self, time: float) -> list[bool, list[int, int]] | None:
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

    def tasks_cost(self) -> list[float, list[int, int]]:
        # Estimate the time required to complete the tasks
        end_pos: float[int, int] = self.pos
        time_estimate: float = 0
        if self.state == DroneState.SCANNING:
            time_estimate += self.scan_rem
        elif self.state == DroneState.MOVING:
            time_estimate += self.distance_rem / self.speed
        if self.state != DroneState.MOVING:
            time_estimate += self.distance(self.pos, self.task_list[0][0]) / self.speed
            if self.task_list[0][1]:
                time_estimate += self.scan_len
        for task in range(1,len(self.task_list)):
            task_distance: float = self.distance(self.task_list[task - 1][0], self.task_list[task][0])
            time_estimate += task_distance / self.speed
            if self.task_list[task][1]:
                time_estimate += self.scan_len
        if len(self.task_list) > 0:
            end_pos = self.task_list[-1][0]
        
        return [time_estimate, end_pos]
    
    def individual_task_cost(self, start: list[int, int], target: list[int, int], scan: bool) -> float:
        # Estimate the time required to complete a specific task
        time_estimate: float = 0
        time_estimate += self.distance(start, target) / self.speed
        if scan:
            time_estimate += self.scan_len
        
        return time_estimate


class ControllerDrone(Drone):
    """A class representing the controller drone"""
    def __init__(self, pos: list[int, int], grid: Grid, drones: list[Drone, Drone, Drone], map: Map) -> None:
        super().__init__(pos, grid)
        self.drones: list[Drone] = drones
        self.map: Map = map
    
    def assign_specific_drone(self, drone: Drone, target: list[int, int], scan: bool) -> None:
        # Assign a specific drone to a target location
        if target[0] < -2 or target[0] >= self.grid.get_length() + 1 or target[1] < 0 or target[1] >= self.grid.get_width():
            raise ValueError("Location out of bounds")
        drone.task_list.append((target, scan))

    def assign_drone(self, target: list[int, int], scan: bool):
        if target[0] < -2 or target[0] >= self.grid.get_length() + 1 or target[1] < 0 or target[1] >= self.grid.get_width():
            raise ValueError("Location out of bounds")
        if (target[0] < 0 and scan) or (target[0] == self.grid.get_length() and scan):
            raise ValueError("Cannot scan start or end location")
        drone_task_lens: list[float, float, float] = [0, 0, 0]
        for drone in range(len(self.drones)):
            drone_tasks: list[float, list[int, int]] = self.drones[drone].tasks_cost()
            drone_task_lens[drone] += drone_tasks[0]
            drone_task_lens[drone] += self.individual_task_cost(drone_tasks[1], target, scan)
        min_drone: int = 0
        for drone in range(1, len(self.drones)):
            if drone_task_lens[drone] < drone_task_lens[min_drone]:
                min_drone = drone
        self.assign_specific_drone(self.drones[min_drone], target, scan)


