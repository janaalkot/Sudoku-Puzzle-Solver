import random
from models.sudoku import Sudoku
from algorithms.backtracking import BacktrackingSolver

class PuzzleGenerator:
    """
    Generates valid Sudoku puzzles of various sizes and difficulties.
    """
    
    @staticmethod
    def generate(size=9, difficulty='medium'):
        """
        Generate a valid Sudoku puzzle.
        
        Args:
            size (int): Size of the grid (4, 9, 16, etc.)
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
            
        Returns:
            Sudoku: A valid puzzle with some cells filled
        """
        # Create a complete valid solution first
        sudoku = Sudoku(size)
        PuzzleGenerator._fill_diagonal_boxes(sudoku)
        
        # Solve it to get a complete valid grid
        solver = BacktrackingSolver(sudoku)
        solver.solve()
        complete_grid = solver.get_solution()
        
        # Remove numbers based on difficulty
        removal_map = {
            'easy': 0.4,    # Remove 40% of cells
            'medium': 0.5,  # Remove 50% of cells
            'hard': 0.6     # Remove 60% of cells
        }
        
        removal_ratio = removal_map.get(difficulty, 0.5)
        cells_to_remove = int(size * size * removal_ratio)
        
        puzzle = Sudoku(size, complete_grid)
        positions = [(r, c) for r in range(size) for c in range(size)]
        random.shuffle(positions)
        
        for i in range(cells_to_remove):
            row, col = positions[i]
            puzzle.grid[row][col] = 0
        
        return puzzle
    
    @staticmethod
    def _fill_diagonal_boxes(sudoku):
        """
        Fill diagonal sub-boxes with random valid numbers.
        This ensures no conflicts initially.
        
        Args:
            sudoku (Sudoku): The puzzle to fill
        """
        box_size = sudoku.box_size
        for box_start in range(0, sudoku.size, box_size):
            PuzzleGenerator._fill_box(sudoku, box_start, box_start)
    
    @staticmethod
    def _fill_box(sudoku, row_start, col_start):
        """
        Fill a single sub-box with random numbers 1 to size.
        
        Args:
            sudoku (Sudoku): The puzzle
            row_start (int): Starting row of the box
            col_start (int): Starting column of the box
        """
        numbers = list(range(1, sudoku.size + 1))
        random.shuffle(numbers)
        
        idx = 0
        for r in range(row_start, row_start + sudoku.box_size):
            for c in range(col_start, col_start + sudoku.box_size):
                sudoku.grid[r][c] = numbers[idx]
                idx += 1
    
    @staticmethod
    def get_sample_puzzles():
        """
        Get a collection of sample puzzles for testing.
        
        Returns:
            dict: Dictionary mapping puzzle names to Sudoku objects
        """
        samples = {}
        
        # Easy 4x4 puzzle
        samples['4x4 Easy'] = Sudoku(4, [
            [1, 0, 0, 2],
            [0, 2, 1, 0],
            [0, 1, 2, 0],
            [2, 0, 0, 1]
        ])
        
        # Easy 6x6 puzzle
        samples['6x6 Easy'] = Sudoku(6, [
            [0, 0, 6, 0, 0, 3],
            [5, 0, 0, 0, 0, 0],
            [0, 1, 3, 4, 0, 0],
            [0, 0, 0, 0, 0, 6],
            [0, 0, 1, 0, 5, 0],
            [0, 0, 0, 1, 0, 0]
        ])
        
        # Medium 6x6 puzzle
        samples['6x6 Medium'] = Sudoku(6, [
            [0, 0, 0, 0, 4, 0],
            [0, 0, 5, 6, 0, 0],
            [4, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 4],
            [0, 0, 6, 5, 0, 0],
            [0, 4, 0, 0, 0, 0]
        ])
        
        # Easy 9x9 puzzle
        samples['9x9 Easy'] = Sudoku(9, [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ])
        
        # Medium 9x9 puzzle
        samples['9x9 Medium'] = Sudoku(9, [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ])
        
        return samples
