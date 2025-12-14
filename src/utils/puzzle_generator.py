import random
from models.sudoku import Sudoku
from algorithms.backtracking import BacktrackingSolver

class PuzzleGenerator:
    
    @staticmethod
    def generate(size=9, difficulty='medium'):
        sudoku = Sudoku(size)
        PuzzleGenerator._fill_diagonal_boxes(sudoku)
        
        solver = BacktrackingSolver(sudoku)
        solver.solve()
        complete_grid = solver.get_solution()
        
        removal_map = {
            'easy': 0.4,
            'medium': 0.5,
            'hard': 0.6
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
        box_size = sudoku.box_size
        for box_start in range(0, sudoku.size, box_size):
            PuzzleGenerator._fill_box(sudoku, box_start, box_start)
    
    @staticmethod
    def _fill_box(sudoku, row_start, col_start):
        numbers = list(range(1, sudoku.size + 1))
        random.shuffle(numbers)
        
        idx = 0
        for r in range(row_start, row_start + sudoku.box_size):
            for c in range(col_start, col_start + sudoku.box_size):
                sudoku.grid[r][c] = numbers[idx]
                idx += 1
    
    @staticmethod
    def get_sample_puzzles():
        samples = {}
        
        samples['4x4 Easy'] = Sudoku(4, [
            [1, 0, 0, 2],
            [0, 2, 1, 0],
            [0, 1, 2, 0],
            [2, 0, 0, 1]
        ])
        
        samples['6x6 Easy'] = Sudoku(6, [
            [0, 0, 6, 0, 0, 3],
            [5, 0, 0, 0, 0, 0],
            [0, 1, 3, 4, 0, 0],
            [0, 0, 0, 0, 0, 6],
            [0, 0, 1, 0, 5, 0],
            [0, 0, 0, 1, 0, 0]
        ])
        
        samples['6x6 Medium'] = Sudoku(6, [
            [0, 0, 0, 0, 4, 0],
            [0, 0, 5, 6, 0, 0],
            [4, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 4],
            [0, 0, 6, 5, 0, 0],
            [0, 4, 0, 0, 0, 0]
        ])
        
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
