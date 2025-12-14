import copy

class Sudoku:
    
    def __init__(self, size=9, grid=None):
        self.size = size
        self.box_size = int(size ** 0.5)
        
        if grid:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def is_valid(self, row, col, num):
        if num in self.grid[row]:
            return False
        
        for r in range(self.size):
            if self.grid[r][col] == num:
                return False
        
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        
        for r in range(box_row, box_row + self.box_size):
            for c in range(box_col, box_col + self.box_size):
                if self.grid[r][c] == num:
                    return False
        
        return True
    
    def find_empty(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return (row, col)
        return None
    
    def is_complete(self):
        return self.find_empty() is None
    
    def get_possible_values(self, row, col):
        if self.grid[row][col] != 0:
            return []
        
        possible = []
        for num in range(1, self.size + 1):
            if self.is_valid(row, col, num):
                possible.append(num)
        return possible
    
    def copy(self):
        return Sudoku(self.size, self.grid)
    
    def __str__(self):
        result = []
        for row in self.grid:
            result.append(" ".join(str(cell) if cell != 0 else "." for cell in row))
        return "\n".join(result)
