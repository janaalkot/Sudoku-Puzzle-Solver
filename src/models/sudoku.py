import copy

class Sudoku:
    """
    Core Sudoku puzzle model that handles puzzle state and validation.
    Supports variable grid sizes (4x4, 6x6, 9x9, etc.)
    """
    
    def __init__(self, size=9, grid=None):
        """
        Initialize a Sudoku puzzle.
        
        Args:
            size (int): Size of the grid (must be a perfect square: 4, 9, 16, etc.)
            grid (list): Optional 2D list representing the initial puzzle state
        """
        self.size = size
        self.box_size = int(size ** 0.5)  # Size of each sub-box (e.g., 3 for 9x9)
        
        if grid:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def is_valid(self, row, col, num):
        """
        Check if placing a number at given position is valid.
        
        Args:
            row (int): Row index
            col (int): Column index
            num (int): Number to place (1 to size)
            
        Returns:
            bool: True if placement is valid, False otherwise
        """
        # Check row
        if num in self.grid[row]:
            return False
        
        # Check column
        for r in range(self.size):
            if self.grid[r][col] == num:
                return False
        
        # Check sub-box
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        
        for r in range(box_row, box_row + self.box_size):
            for c in range(box_col, box_col + self.box_size):
                if self.grid[r][c] == num:
                    return False
        
        return True
    
    def find_empty(self):
        """
        Find the next empty cell (containing 0).
        
        Returns:
            tuple: (row, col) of empty cell, or None if no empty cells
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None
    
    def is_complete(self):
        """
        Check if the puzzle is completely filled.
        
        Returns:
            bool: True if all cells are filled, False otherwise
        """
        return self.find_empty() is None
    
    def get_possible_values(self, row, col):
        """
        Get all valid values for a given cell.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            list: List of valid numbers for the cell
        """
        if self.grid[row][col] != 0:
            return []
        
        possible = []
        for num in range(1, self.size + 1):
            if self.is_valid(row, col, num):
                possible.append(num)
        return possible
    
    def copy(self):
        """
        Create a deep copy of the puzzle.
        
        Returns:
            Sudoku: New Sudoku instance with copied grid
        """
        return Sudoku(self.size, self.grid)
    
    def __str__(self):
        """String representation of the puzzle for debugging."""
        result = []
        for row in self.grid:
            result.append(" ".join(str(cell) if cell != 0 else "." for cell in row))
        return "\n".join(result)
