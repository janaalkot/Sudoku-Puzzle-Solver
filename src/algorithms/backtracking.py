from models.sudoku import Sudoku

class BacktrackingSolver:
    """
    Solves Sudoku puzzles using the Backtracking Algorithm.
    This is a depth-first search approach that tries values and backtracks on conflicts.
    """
    
    def __init__(self, sudoku):
        """
        Initialize the solver with a Sudoku puzzle.
        
        Args:
            sudoku (Sudoku): The Sudoku puzzle to solve
        """
        self.sudoku = sudoku.copy()
        self.iterations = 0
        self.steps = []  # Store (action, row, col, value) for visualization
        self.backtrack_count = 0
        self.visualization_callback = None
    
    def solve(self, collect_steps=False, callback=None):
        """
        Solve the Sudoku puzzle using backtracking.
        
        Args:
            collect_steps (bool): Whether to collect steps for visualization
            callback (callable): Optional callback function(action, row, col, value, grid)
                                called after each step for real-time visualization
            
        Returns:
            bool: True if solved, False if unsolvable
        """
        self.iterations = 0
        self.backtrack_count = 0
        self.visualization_callback = callback
        if collect_steps or callback:
            self.steps = []
        
        return self._backtrack(collect_steps or callback is not None)
    
    def _backtrack(self, collect_steps):
        """
        Recursive backtracking helper function.
        
        Args:
            collect_steps (bool): Whether to collect steps for visualization
            
        Returns:
            bool: True if solution found, False otherwise
        """
        self.iterations += 1
        
        # Find next empty cell
        empty = self.sudoku.find_empty()
        if empty is None:
            return True  # Puzzle solved
        
        row, col = empty
        
        # Try each possible value
        for num in range(1, self.sudoku.size + 1):
            # Show attempt (even if not valid) for visualization
            if collect_steps and self.visualization_callback:
                import copy
                # First show the attempt
                self.visualization_callback('attempt', row, col, num, 
                                           copy.deepcopy(self.sudoku.grid))
            
            if self.sudoku.is_valid(row, col, num):
                # Place number (valid placement)
                self.sudoku.grid[row][col] = num
                
                if collect_steps:
                    self.steps.append(('place', row, col, num))
                    if self.visualization_callback:
                        import copy
                        self.visualization_callback('place', row, col, num, 
                                                   copy.deepcopy(self.sudoku.grid))
                
                # Recursively try to solve
                if self._backtrack(collect_steps):
                    return True
                
                # Backtrack: remove number
                self.sudoku.grid[row][col] = 0
                self.backtrack_count += 1
                
                if collect_steps:
                    self.steps.append(('backtrack', row, col, 0))
                    if self.visualization_callback:
                        import copy
                        self.visualization_callback('backtrack', row, col, 0, 
                                                   copy.deepcopy(self.sudoku.grid))
            else:
                # Invalid placement - show rejection
                if collect_steps and self.visualization_callback:
                    import copy
                    self.visualization_callback('reject', row, col, num, 
                                               copy.deepcopy(self.sudoku.grid))
        
        return False
    
    def get_solution(self):
        """
        Get the solved puzzle grid.
        
        Returns:
            list: 2D list representing the solved puzzle
        """
        return self.sudoku.grid
    
    def get_metrics(self):
        """
        Get performance metrics.
        
        Returns:
            dict: Dictionary containing iterations and backtrack count
        """
        return {
            'iterations': self.iterations,
            'backtracks': self.backtrack_count,
            'algorithm': 'Backtracking'
        }