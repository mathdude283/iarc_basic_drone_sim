class Map:
    """A class representing the current drone positions and mapped out area."""
    def __init__(self, mfld_length: int, mfld_width: int) -> None:
        """Initialize the map with the given length and width."""
        self.mfld_length: int = mfld_length
        self.mfld_width: int = mfld_width
        self.length: int = self.mfld_length + 3