from tile_state import TileState

class Map:
    """A class representing the current drone positions and mapped out area."""
    def __init__(self, mfld_length: int, mfld_width: int) -> None:
        """Initialize the map with the given length and width."""
        self.mfld_length: int = mfld_length
        self.mfld_width: int = mfld_width
        self.length: int = self.mfld_length + 3
        self.start = [TileState.SAFE for _ in range(self.mfld_width)]
        self.end = [[TileState.SAFE for _ in range(self.mfld_width)] for _ in range(2)]
        self.map = [[TileState.UNKNOWN for _ in range(self.mfld_width)] for _ in range(self.mfld_length)]

    def get_tile_status(self, loc: list[int, int]) -> TileState:
        """Gets the status of a tile"""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        return self.map[loc[0]][loc[1]]
    
    def queue_tile(self, loc: list[int, int]) -> None:
        """Queues a tile for scanning."""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        if self.map[loc[0]][loc[1]] != TileState.UNKNOWN:
            raise ValueError("Tile already scanned or queued")
        self.map[loc[0]][loc[1]] = TileState.QUEUED
    
    def scan_tile(self, loc: list[int, int]) -> None:
        """Scans a tile."""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        if self.map[loc[0]][loc[1]] != TileState.QUEUED:
            raise ValueError("Tile not queued for scanning")
        self.map[loc[0]][loc[1]] = TileState.SCANNING
    
    def mark_safe(self, loc: list[int, int]) -> None:
        """Marks a tile as safe."""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        if self.map[loc[0]][loc[1]] == TileState.UNKNOWN or self.map[loc[0]][loc[1]] == TileState.QUEUED:
            raise ValueError("Tile not yet scanned")
        if self.map[loc[0]][loc[1]] == TileState.SAFE:
            raise ValueError("Tile already marked safe")
        if self.map[loc[0]][loc[1]] == TileState.MINE or self.map[loc[0]][loc[1]] == TileState.UNSAFE:
            raise ValueError("Tile known to be unsafe")
        self.map[loc[0]][loc[1]] = TileState.SAFE
    
    def mark_mine(self, loc: list[int, int]) -> None:
        """Marks a tile as a mine."""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        if self.map[loc[0]][loc[1]] == TileState.UNKNOWN or self.map[loc[0]][loc[1]] == TileState.QUEUED:
            raise ValueError("Tile not yet scanned")
        if self.map[loc[0]][loc[1]] == TileState.MINE:
            raise ValueError("Tile already marked as mine")
        if self.map[loc[0]][loc[1]] == TileState.SAFE:
            raise ValueError("Tile known to be safe")
        self.map[loc[0]][loc[1]] = TileState.MINE

    def mark_unsafe(self, loc: list[int, int]) -> None:
        """Marks a tile as unsafe."""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        if self.map[loc[0]][loc[1]] == TileState.UNKNOWN or self.map[loc[0]][loc[1]] == TileState.QUEUED:
            raise ValueError("Tile not yet scanned")
        if self.map[loc[0]][loc[1]] == TileState.MINE:
            raise ValueError("Tile already known to be a mine")
        if self.map[loc[0]][loc[1]] == TileState.SAFE:
            raise ValueError("Tile already marked safe")
        self.map[loc[0]][loc[1]] = TileState.UNSAFE 
    
    def finish_scan(self, loc: list[int, int], status: TileState) -> None:
        """Finishes scanning a tile."""
        if loc[0] < 0 or loc[0] >= self.mfld_length or loc[1] < 0 or loc[1] >= self.mfld_width:
            raise ValueError("Location out of bounds")
        if self.map[loc[0]][loc[1]] != TileState.SCANNING:
            raise ValueError("Tile not currently scanning")
        if status == TileState.UNKNOWN or status == TileState.QUEUED or status == TileState.SCANNING:
            raise ValueError("Invalid Scan Status")
        self.map[loc[0]][loc[1]] = status

    def get_tile_repr(self, tile: TileState) -> str:
        """Get the string representation of a tile."""
        if tile == TileState.UNKNOWN:
            return "?"
        elif tile == TileState.SAFE:
            return "O"
        elif tile == TileState.MINE:
            return "X"
        elif tile == TileState.QUEUED:
            return "Q"
        elif tile == TileState.SCANNING:
            return "S"
        else:
            raise ValueError(f"Unknown tile state: {tile}")

    def print_map(self) -> None:
        """Prints the current status of the map."""

        print("Map:")
        for row in self.end:
            for cell in row:
                print(self.get_tile_repr(cell), end=" ")
            print()
        for _ in range(self.mfld_width * 2 - 1):
            print("-", end="")
        print()

        for row in self.map:
            for cell in row:
                print(self.get_tile_repr(cell), end=" ")
            print()
        for _ in range(self.mfld_width * 2 - 1):
            print("-", end="")
        print()

        for cell in self.start:
            print(self.get_tile_repr(cell), end=" ")
        print()
        print()
