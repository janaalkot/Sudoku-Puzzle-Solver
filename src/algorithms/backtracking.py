from models.sudoku import Sudoku

class BacktrackingSolver:
    
    def __init__(self, sudoku):
        self.sudoku = sudoku.copy()
        self.iterations = 0
        self.steps = []
        self.backtrack_count = 0
        self.visualization_callback = None
    
    def solve(self, collect_steps=False, callback=None):
        self.iterations = 0
        self.backtrack_count = 0
        self.visualization_callback = callback
        if collect_steps or callback:
            self.steps = []
        
        return self._backtrack(collect_steps or callback is not None)
    
    def _backtrack(self, collect_steps):
        self.iterations += 1
        
        empty = self.sudoku.find_empty()
        if empty is None:
            return True
        
        row, col = empty
        
        for num in range(1, self.sudoku.size + 1):
            if collect_steps and self.visualization_callback:
                import copy
                self.visualization_callback('attempt', row, col, num, 
                                           copy.deepcopy(self.sudoku.grid))
            
            if self.sudoku.is_valid(row, col, num):
                self.sudoku.grid[row][col] = num
                
                if collect_steps:
                    self.steps.append(('place', row, col, num))
                    if self.visualization_callback:
                        import copy
                        self.visualization_callback('place', row, col, num, 
                                                   copy.deepcopy(self.sudoku.grid))
                
                if self._backtrack(collect_steps):
                    return True
                
                self.sudoku.grid[row][col] = 0
                self.backtrack_count += 1
                
                if collect_steps:
                    self.steps.append(('backtrack', row, col, 0))
                    if self.visualization_callback:
                        import copy
                        self.visualization_callback('backtrack', row, col, 0, 
                                                   copy.deepcopy(self.sudoku.grid))
            else:
                if collect_steps and self.visualization_callback:
                    import copy
                    self.visualization_callback('reject', row, col, num, 
                                               copy.deepcopy(self.sudoku.grid))
        
        return False
    
    def get_solution(self):
        return self.sudoku.grid
    
    def get_metrics(self):
        return {
            'iterations': self.iterations,
            'backtracks': self.backtrack_count,
            'algorithm': 'Backtracking'
        }