# Sudoku Puzzle Solver - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Module Documentation](#module-documentation)
4. [Algorithm Details](#algorithm-details)
5. [Performance Notes](#performance-notes)
6. [Troubleshooting](#troubleshooting)

---

## Overview

This project implements an intelligent Sudoku puzzle solver using Python and Tkinter. It features two distinct solving algorithms:

1. **Backtracking Algorithm** - A depth-first search approach with constraint satisfaction
2. **Cultural Algorithm** - An evolutionary computation technique with belief space

The application provides a modern, interactive GUI with step-by-step visualization, multiple grid sizes (4x4, 6x6, 9x9), and real-time performance metrics.

---

## Project Structure

### Folder Structure Diagram

```
Sudoku-Puzzle-Solver/
│
├── src/                              # Source code directory
│   ├── models/                       # Data models
│   │   ├── __init__.py
│   │   └── sudoku.py                # Core Sudoku model class
│   │
│   ├── algorithms/                   # Solving algorithms
│   │   ├── __init__.py
│   │   ├── backtracking.py          # Backtracking solver
│   │   └── cultural.py              # Cultural Algorithm solver
│   │
│   ├── gui/                          # User interface
│   │   ├── __init__.py
│   │   ├── gui.py                   # Main GUI application
│   │   └── styles.py                # Visual styling system
│   │
│   ├── utils/                        # Utility modules
│   │   ├── __init__.py
│   │   └── puzzle_generator.py      # Puzzle generation utilities
│   │
│   ├── docs/                         # Documentation
│   │   └── documentation.md         # This file
│   │
│   └── main.py                       # Application entry point
│
├── run.py                            # Launcher script
├── README.md                         # Project overview
└── .gitignore                        # Git ignore rules
```

### Visual Tree Structure

```
┌─────────────────────────────────────────────────────────────┐
│              Sudoku-Puzzle-Solver (Root)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┬────────────┐
         │             │             │            │
    ┌────▼───┐   ┌────▼────┐   ┌───▼───┐   ┌───▼──────┐
    │  src/  │   │ run.py  │   │README │   │.gitignore│
    └────┬───┘   └─────────┘   └───────┘   └──────────┘
         │
    ┌────┼────────┬────────┬──────┬──────┐
    │    │        │        │      │      │
┌───▼──┐│  ┌────▼───┐  ┌──▼──┐ ┌─▼──┐ ┌─▼─────┐
│models││  │algorithms│ gui    │|utils│ docs  │
└──┬───┘│  └────┬─────┘└──┬──┘ └──┬──┘└──┬────┘
   │    │       │          │      │      │
   │ ┌──▼───┐  │     ┌────▼──┐   │      │
   │ │main.py  │     │styles.│   │      │
   │ └──────┘  │     │py     │   │      │
   │           │     └───────┘   │      │
┌──▼────┐  ┌──▼──────┐  ┌───────▼─┐ ┌──▼────────┐
│sudoku.│  │backtrac-│  │cultural.│ │puzzle_    │
│py     │  │king.py  │  │py       │ │generator. │
└───────┘  └─────────┘  └─────────┘ │py         │
                                     └───────────┘
```

---

## Module Documentation

### 1. models/sudoku.py

**Purpose**: Core Sudoku puzzle representation with validation and utility methods.

#### Class: `Sudoku`

Represents a Sudoku puzzle with complete validation logic and helper methods.

##### Constructor

```python
__init__(self, size=9, grid=None)
```

**Parameters**:

- `size` (int): Size of the grid. Must be a perfect square (4, 9, 16, 25, etc.)
  - 4 → 2×2 sub-boxes
  - 9 → 3×3 sub-boxes
  - 16 → 4×4 sub-boxes
- `grid` (list, optional): 2D list (size × size) representing initial puzzle. Use 0 for empty cells.

**Description**: Initializes a Sudoku puzzle. Calculates box_size automatically as √size.

**Example**:

```python
# Create 9x9 puzzle
puzzle = Sudoku(9, [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    # ... more rows
])

# Create empty 4x4 puzzle
small_puzzle = Sudoku(4)
```

---

##### Methods

```python
is_valid(self, row, col, num) -> bool
```

**Parameters**:

- `row` (int): Row index (0-based, 0 to size-1)
- `col` (int): Column index (0-based, 0 to size-1)
- `num` (int): Number to validate (1 to size)

**Returns**: `True` if placing `num` at `(row, col)` doesn't violate Sudoku rules, `False` otherwise.

**Description**: Checks three constraints:

1. No duplicate in the same row
2. No duplicate in the same column
3. No duplicate in the same sub-box

**Example**:

```python
if puzzle.is_valid(0, 2, 5):
    puzzle.grid[0][2] = 5
```

---

```python
find_empty(self) -> tuple | None
```

**Parameters**: None

**Returns**:

- Tuple `(row, col)` of the first empty cell (containing 0)
- `None` if no empty cells exist

**Description**: Scans left-to-right, top-to-bottom to find first empty cell.

**Example**:

```python
empty = puzzle.find_empty()
if empty:
    row, col = empty
    print(f"Empty cell at ({row}, {col})")
```

---

```python
is_complete(self) -> bool
```

**Parameters**: None

**Returns**: `True` if all cells are filled (no zeros), `False` otherwise.

**Description**: Quick check if puzzle has any remaining empty cells.

**Example**:

```python
if puzzle.is_complete():
    print("Puzzle is filled!")
```

---

```python
get_possible_values(self, row, col) -> list
```

**Parameters**:

- `row` (int): Row index
- `col` (int): Column index

**Returns**: List of integers (1 to size) that can be validly placed at the position.

**Description**: Returns all numbers that don't violate row, column, or box constraints. Returns empty list if cell is already filled.

**Example**:

```python
possible = puzzle.get_possible_values(0, 2)
print(f"Can place: {possible}")  # e.g., [1, 4, 6, 8]
```

---

```python
copy(self) -> Sudoku
```

**Parameters**: None

**Returns**: New `Sudoku` instance with deep-copied grid.

**Description**: Creates independent copy. Modifications to copy don't affect original.

**Example**:

```python
backup = puzzle.copy()
# Try something with puzzle, restore from backup if needed
```

---

```python
__str__(self) -> str
```

**Parameters**: None

**Returns**: String representation of puzzle (for debugging).

**Description**: Returns grid with dots (.) for empty cells, numbers for filled cells.

**Example**:

```python
print(puzzle)
# Output:
# 5 3 . . 7 . . . .
# 6 . . 1 9 5 . . .
```

---

### 2. algorithms/backtracking.py

**Purpose**: Implements depth-first search with backtracking for guaranteed Sudoku solving.

#### Class: `BacktrackingSolver`

Uses recursive backtracking to systematically try all possibilities.

##### Constructor

```python
__init__(self, sudoku)
```

**Parameters**:

- `sudoku` (Sudoku): The puzzle to solve (will be copied internally)

**Description**: Initializes solver with a copy of the puzzle. Tracks iterations and backtrack count.

**Attributes**:

- `sudoku`: Working copy of puzzle
- `iterations`: Total cell placement attempts
- `backtrack_count`: Number of times algorithm backed up
- `steps`: List of steps for visualization
- `visualization_callback`: Optional callback function

---

##### Methods

```python
solve(self, collect_steps=False, callback=None) -> bool
```

**Parameters**:

- `collect_steps` (bool): Whether to collect steps for visualization
- `callback` (callable, optional): Visualization callback with signature:
  ```python
  callback(action, row, col, value, grid)
  ```
  Where:
  - `action` (str): 'attempt', 'reject', 'place', or 'backtrack'
  - `row` (int): Current row
  - `col` (int): Current column
  - `value` (int): Number being tried
  - `grid` (list): Current grid state (deep copy)

**Returns**: `True` if puzzle is solvable, `False` if no solution exists.

**Description**: Solves puzzle using recursive backtracking:

1. Find empty cell
2. Try numbers 1 through size
3. For each valid number:
   - Place it and recurse
   - If recursion succeeds, done
   - Otherwise, backtrack (remove number)
4. If no numbers work, return False

**Example**:

```python
solver = BacktrackingSolver(puzzle)

# Solve without visualization
if solver.solve():
    print("Solved!")
    solution = solver.get_solution()

# Solve with visualization
def visualize(action, row, col, val, grid):
    print(f"{action}: ({row},{col}) = {val}")

solver.solve(callback=visualize)
```

---

```python
get_solution(self) -> list
```

**Parameters**: None

**Returns**: 2D list (size × size) representing the solved puzzle grid.

**Description**: Returns current state of internal grid. Should be called after `solve()`.

**Example**:

```python
if solver.solve():
    solution = solver.get_solution()
    for row in solution:
        print(row)
```

---

```python
get_metrics(self) -> dict
```

**Parameters**: None

**Returns**: Dictionary with performance metrics:

```python
{
    'algorithm': 'Backtracking',
    'iterations': int,     # Total placement attempts
    'backtracks': int      # Number of backtrack operations
}
```

**Description**: Provides statistics about the solving process.

**Example**:

```python
metrics = solver.get_metrics()
print(f"Solved in {metrics['iterations']} iterations")
print(f"Backtracked {metrics['backtracks']} times")
```

---

### 3. algorithms/cultural.py

**Purpose**: Implements Cultural Algorithm - an evolutionary approach with belief space.

#### Class: `CulturalAlgorithmSolver`

Uses population evolution and accumulated cultural knowledge to solve Sudoku.

##### Constructor

```python
__init__(self, sudoku, population_size=50, max_generations=1000)
```

**Parameters**:

- `sudoku` (Sudoku): The puzzle to solve
- `population_size` (int, default=50): Number of candidate solutions in population
- `max_generations` (int, default=1000): Maximum evolution cycles

**Description**: Initializes Cultural Algorithm with:

- **Population Space**: Set of candidate solutions
- **Belief Space**: Accumulated knowledge about good values at each position
- **Fixed Cells**: Tracks which cells cannot be modified (given clues)

**Attributes**:

- `original`: Copy of initial puzzle
- `size`: Grid size
- `fixed_cells`: Set of (row, col) tuples for pre-filled cells
- `belief_space`: Dictionary mapping (row, col) to list of good values
- `iterations`: Generation counter
- `best_fitness`: Best fitness score achieved (0 = solved)
- `best_solution`: Best solution found

---

##### Methods

```python
solve(self, collect_steps=False, callback=None) -> bool
```

**Parameters**:

- `collect_steps` (bool): Whether to collect steps (for compatibility)
- `callback` (callable, optional): Visualization callback with signature:
  ```python
  callback(generation, best_grid, best_fitness) -> bool
  ```
  Where:
  - `generation` (int): Current generation number
  - `best_grid` (list): 2D list of best solution so far
  - `best_fitness` (int): Fitness score (0 = perfect)
  - Return `False` to stop evolution early

**Returns**: `True` if perfect solution found (fitness=0), `False` otherwise.

**Description**: Evolution process:

1. Initialize random population with row-permutation strategy
2. For each generation:
   - Evaluate fitness of all individuals
   - Update belief space from elite individuals (top 20%)
   - Preserve elite (elitism)
   - Create offspring via tournament selection, crossover, mutation
   - Check for solution (fitness = 0)
3. Return best solution (may not be perfect)

**Example**:

```python
solver = CulturalAlgorithmSolver(puzzle,
                                  population_size=100,
                                  max_generations=1000)

# Solve without visualization
success = solver.solve()
solution = solver.get_solution()

# Solve with visualization
def visualize(gen, grid, fitness):
    print(f"Gen {gen}: fitness = {fitness}")
    return True  # Continue

solver.solve(callback=visualize)
```

---

```python
get_solution(self) -> list
```

**Parameters**: None

**Returns**: 2D list (size × size) of best solution found.

**Description**: Returns best solution discovered during evolution. May not be perfect (fitness > 0).

**Example**:

```python
solution = solver.get_solution()
fitness = solver.best_fitness
if fitness == 0:
    print("Perfect solution!")
else:
    print(f"Best approximation (fitness={fitness})")
```

---

```python
get_metrics(self) -> dict
```

**Parameters**: None

**Returns**: Dictionary with performance metrics:

```python
{
    'algorithm': 'Cultural Algorithm',
    'iterations': int,      # Number of generations
    'best_fitness': int     # Best fitness (0 = solved)
}
```

**Description**: Provides evolution statistics.

**Example**:

```python
metrics = solver.get_metrics()
print(f"Evolved for {metrics['iterations']} generations")
print(f"Best fitness: {metrics['best_fitness']}")
```

---

##### Private Methods (Internal Use)

```python
_get_fixed_cells(self, sudoku) -> set
```

**Description**: Returns set of (row, col) tuples for cells with pre-filled values (clues).

---

```python
_initialize_belief_space(self) -> dict
```

**Description**: Creates initial belief space mapping each empty cell to its possible values.

---

```python
_create_individual(self) -> Sudoku
```

**Description**: Creates random candidate solution using row-permutation initialization:

- Each row contains numbers 1-size exactly once
- Reduces constraint violations significantly
- Better than random cell-by-cell filling

---

```python
_fitness(self, individual) -> int
```

**Description**: Calculates fitness (lower is better):

- Counts duplicate numbers in each row
- Counts duplicate numbers in each column
- Counts duplicate numbers in each box
- Returns total violations (0 = perfect solution)

---

```python
_crossover(self, parent1, parent2) -> Sudoku
```

**Description**: Creates offspring by row-based crossover:

- For each row, randomly choose from parent1 or parent2
- Preserves row structure better than cell-wise crossover

---

```python
_mutate(self, individual, mutation_rate=0.15)
```

**Description**: Mutates individual by swapping values within rows:

- For each row, with probability `mutation_rate`:
  - Swap two random non-fixed cells in that row
- Preserves row validity

---

```python
_update_belief_space(self, population)
```

**Description**: Updates belief space from elite individuals:

- Takes top 20% of population
- Records which values appear frequently at each position
- Guides future individual creation

---

### 4. utils/puzzle_generator.py

**Purpose**: Generates random Sudoku puzzles and provides sample puzzles.

#### Class: `PuzzleGenerator`

Static utility class for puzzle creation.

##### Static Methods

```python
@staticmethod
generate(size=9, difficulty='medium') -> Sudoku
```

**Parameters**:

- `size` (int): Grid size (4, 6, or 9)
- `difficulty` (str): 'easy', 'medium', or 'hard'

**Returns**: `Sudoku` object with generated puzzle.

**Description**: Generation process:

1. Create empty grid
2. Fill diagonal boxes with random valid numbers
3. Solve to get complete valid solution
4. Remove cells based on difficulty:
   - Easy: 40% removed
   - Medium: 50% removed
   - Hard: 60% removed

**Example**:

```python
# Generate medium 9x9 puzzle
puzzle = PuzzleGenerator.generate(9, 'medium')

# Generate easy 4x4 puzzle
small = PuzzleGenerator.generate(4, 'easy')
```

---

```python
@staticmethod
get_sample_puzzles() -> dict
```

**Parameters**: None

**Returns**: Dictionary mapping puzzle names (str) to `Sudoku` objects.

**Description**: Returns predefined puzzles:

- `'4x4 Easy'`
- `'6x6 Easy'`
- `'6x6 Medium'`
- `'9x9 Easy'`
- `'9x9 Medium'`

**Example**:

```python
samples = PuzzleGenerator.get_sample_puzzles()
puzzle = samples['9x9 Easy']
```

---

```python
@staticmethod
_fill_diagonal_boxes(sudoku)
```

**Description**: Fills diagonal sub-boxes with random permutations (internal helper).

---

```python
_fill_box(sudoku, row_start, col_start)
```

**Description**: Fills single sub-box with shuffled 1-to-size values (internal helper).

---

### 5. gui/styles.py

**Purpose**: Comprehensive styling system for modern, professional UI.

#### Class: `SudokuStyles`

Manages all colors, fonts, and widget styles.

##### Class Attributes

```python
COLORS = {
    # Primary colors
    'primary': '#1976D2',           # Deep blue
    'primary_dark': '#1565C0',      # Darker blue
    'primary_light': '#42A5F5',     # Light blue
    'accent': '#FF9800',            # Orange accent

    # Backgrounds
    'bg_main': '#F5F5F5',           # Light gray
    'bg_panel': '#FFFFFF',          # White
    'bg_grid': '#FAFAFA',           # Very light gray
    'bg_fixed': '#E3F2FD',          # Light blue for clues

    # Cell states
    'cell_attempt': '#FFF9C4',      # Yellow (testing)
    'cell_reject': '#F44336',       # Red (invalid)
    'cell_place': '#4CAF50',        # Green (placed)
    'cell_backtrack': '#FFCDD2',    # Light red (backtrack)
    'cell_solution': '#2196F3',     # Blue (final solution)
    'cell_cultural': '#FF9800',     # Orange (CA evolution)

    # Text colors
    'text_primary': '#212121',      # Dark gray
    'text_secondary': '#757575',    # Medium gray
    'text_light': '#FFFFFF',        # White
    'text_fixed': '#0D47A1',        # Dark blue

    # ... more colors
}
```

```python
FONTS = {
    'title': ('Segoe UI', 16, 'bold'),
    'heading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'cell_normal': ('Arial', 18, 'bold'),
    # ... more fonts
}
```

---

##### Methods

```python
__init__(self, root)
```

**Parameters**:

- `root` (tk.Tk): Root Tkinter window

**Description**: Initializes styling system and applies theme to all ttk widgets.

---

```python
create_cell_style(self, cell_widget, state='normal', is_fixed=False)
```

**Parameters**:

- `cell_widget` (tk.Entry): Grid cell Entry widget
- `state` (str): Visual state:
  - `'normal'`: Default empty cell
  - `'attempt'`: Yellow (testing number)
  - `'reject'`: Red (invalid number)
  - `'place'`: Green (valid placement)
  - `'backtrack'`: Light red (backtracking)
  - `'solution'`: Blue (final answer)
  - `'cultural'`: Orange (CA evolution)
- `is_fixed` (bool): Whether cell contains original clue

**Description**: Applies color scheme and fonts to grid cells.

---

```python
create_text_widget_style(self, text_widget)
```

**Parameters**:

- `text_widget` (tk.Text): Text display widget

**Description**: Styles metrics display area.

---

```python
create_status_bar_style(self, label_widget)
```

**Parameters**:

- `label_widget` (ttk.Label): Status bar label

**Description**: Styles bottom status bar.

---

### 6. gui/gui.py

**Purpose**: Main GUI application with complete user interface.

#### Class: `SudokuGUI`

Manages entire application interface and user interactions.

##### Constructor

```python
__init__(self, root)
```

**Parameters**:

- `root` (tk.Tk): Root Tkinter window

**Description**: Initializes GUI:

- Creates all widgets
- Loads default puzzle
- Sets up event handlers
- Initializes visualization state

**Window Size**: 1200×900 pixels (minimum 1100×850)

---

##### Key Methods

```python
_create_widgets(self)
```

**Description**: Creates complete UI:

- Top control panel (size selector, sample selector, buttons)
- Main area split: grid (left) + controls (right)
- Algorithm selection radio buttons
- Visualization controls (speed sliders)
- Control buttons (Solve, Pause, Stop)
- Metrics display
- Status bar

---

```python
_create_grid(self)
```

**Description**: Creates Sudoku grid with:

- Entry widgets for each cell
- Thicker borders (2px) separating sub-boxes
- Thin borders (1px) between cells
- Dark border color (#2c3e50)
- Internal padding for larger cells
- Input validation

---

```python
_validate_input(self, row, col)
```

**Description**: Validates user input:

- Only allows digits 1 to grid size
- Rejects invalid input immediately

---

```python
_solve_puzzle(self)
```

**Description**: Main solve trigger:

- Gets current puzzle from grid
- Checks if already complete
- Starts solving thread (if visualization enabled)
- Or solves instantly (if visualization disabled)

---

```python
_solve_backtracking_visualized(self, puzzle)
```

**Description**: Backtracking with visualization:

- Shows each attempt (yellow)
- Shows rejections (red)
- Shows placements (green)
- Shows backtracks (light red)
- Updates metrics every 5 steps
- Adaptive speed based on action type

---

```python
_solve_cultural_visualized(self, puzzle)
```

**Description**: Cultural Algorithm with visualization:

- Shows best solution evolving over generations
- Updates every 1/5/10 generations (adaptive)
- Tracks stuck state (no improvement for 20+ generations)
- Adaptive delay (slower early, faster later)
- Shows generation number and fitness in status

---

```python
_display_solution(self, solution)
```

**Description**: Shows final solution:

- Displays all numbers
- Original clues: dark blue on light blue background
- Solution cells: blue text on white background

---

```python
_display_metrics(self, metrics)
```

**Description**: Shows performance statistics:

- Algorithm name
- Iterations/generations
- Backtracks (for Backtracking)
- Best fitness (for Cultural Algorithm)
- Execution time

---

```python
_toggle_pause(self)
```

**Description**: Pauses/resumes solving during visualization.

---

```python
_stop_solving(self)
```

**Description**: Stops solving process immediately.

---

### 7. main.py

**Purpose**: Application entry point.

```python
def main():
    """Launch the Sudoku Solver GUI application."""
    gui_main()
```

**Description**: Simple entry point that launches the GUI.

---

## Algorithm Details

### Backtracking Algorithm

**Type**: Exact algorithm (always finds solution if exists)

**Time Complexity**: O(N^M) where:

- N = grid size
- M = number of empty cells

**Space Complexity**: O(M) for recursion stack

**How It Works**:

1. Find first empty cell
2. Try numbers 1 through N
3. For each number:
   - Check if valid (no row/column/box duplicates)
   - If valid, place it
   - Recursively solve rest of puzzle
   - If successful, done
   - Otherwise, remove number (backtrack)
4. If no numbers work, return failure

**Strengths**:

- ✅ Always finds solution
- ✅ Very fast for easy/medium puzzles (< 1 second)
- ✅ Deterministic
- ✅ Simple logic

**Weaknesses**:

- ❌ Can be slow for very difficult puzzles
- ❌ Explores many dead ends

**Best For**: Guaranteed solutions, fast solving

---

### Cultural Algorithm

**Type**: Heuristic algorithm (may not find perfect solution)

**Time Complexity**: O(P × G × N²) where:

- P = population size (100)
- G = generations (1000)
- N = grid size

**Space Complexity**: O(P × N²) for population

**How It Works**:

1. **Initialize Population**: Create 100 random candidates using row-permutation
2. **For Each Generation**:
   - **Evaluate**: Calculate fitness (count violations)
   - **Select Elite**: Take top 20% of population
   - **Update Belief Space**: Record which values work well where
   - **Elitism**: Keep best 10% unchanged
   - **Selection**: Tournament selection (choose best of 3 random)
   - **Crossover**: Row-based crossover between parents
   - **Mutation**: Swap values within rows (15% probability)
   - **Check Solution**: If fitness = 0, done
3. **Random Restart**: Every 200 generations, replace worst half if stuck

**Components**:

- **Population Space**: 100 candidate solutions evolving
- **Belief Space**: Knowledge about which values work at each position
- **Fitness Function**: Counts duplicates in rows, columns, boxes

**Strengths**:

- ✅ Good at exploring solution space
- ✅ Uses learned knowledge (belief space)
- ✅ Can escape local optima (random restart)
- ✅ Interesting to watch evolve

**Weaknesses**:

- ❌ May not find perfect solution
- ❌ Slower than backtracking
- ❌ Non-deterministic

**Best For**: Exploring alternatives, educational purposes

---

## Performance Notes

### Backtracking Performance

| Grid Size | Difficulty | Typical Time | Iterations |
| --------- | ---------- | ------------ | ---------- |
| 4×4       | Any        | < 0.01s      | < 50       |
| 6×6       | Easy       | < 0.1s       | < 500      |
| 6×6       | Medium     | 0.1-0.5s     | 500-2000   |
| 9×9       | Easy       | 0.01-0.1s    | 100-1000   |
| 9×9       | Medium     | 0.1-1s       | 1000-5000  |
| 9×9       | Hard       | 1-10s        | 5000-50000 |

**Backtracks**: Usually 20-50% of total iterations

---

### Cultural Algorithm Performance

| Grid Size | Typical Time | Generations | Success Rate |
| --------- | ------------ | ----------- | ------------ |
| 4×4       | 1-5s         | 50-200      | ~95%         |
| 6×6       | 5-15s        | 200-500     | ~70%         |
| 9×9       | 10-30s       | 300-1000    | ~40%         |

**Best Fitness**: 0 = perfect, 2-5 = very close, 10+ = needs more evolution

---

## Troubleshooting

### Common Issues

#### Cultural Algorithm Appears Stuck

**Symptoms**: Display not changing, same fitness for many generations

**Causes**:

- Algorithm is fine-tuning near-optimal solution
- Display updates throttled (updates every 5-10 generations)
- Genuinely stuck in local optimum

**Solutions**:

- ✅ Wait longer (up to 1000 generations)
- ✅ Check status bar for "searching..." message
- ✅ Use Stop button and check final fitness
- ✅ If fitness > 0, try Backtracking for guaranteed solution
- ✅ Increase population size or generations in code

---

#### Fitness Not Reaching Zero

**Symptoms**: CA finishes but fitness = 2-10

**Causes**:

- Puzzle is difficult for evolutionary approach
- Got stuck in local optimum
- Need more generations or larger population

**Solutions**:

- ✅ Accept near-optimal solution (fitness < 5 is very good)
- ✅ Use Backtracking for perfect solution
- ✅ Try solving again (different random initialization)
- ✅ Check if puzzle is actually solvable

---

#### Visualization Too Fast/Slow

**Solutions**:

- ✅ Adjust "Action Speed" slider (placement, backtracking)
- ✅ Adjust "Check Speed" slider (number testing)
- ✅ Disable visualization for instant solving
- ✅ Use Pause button to examine states

---

#### Application Won't Start

**Causes**:

- Missing tkinter
- Wrong Python version
- Import errors

**Solutions**:

```bash
# Check Python version
python --version  # Need 3.7+

# Test tkinter
python -m tkinter

# Run from correct directory
cd Sudoku-Puzzle-Solver
python run.py
```

---

#### Grid Display Issues

**Causes**:

- Window too small
- Font issues
- Border rendering

**Solutions**:

- ✅ Ensure window >= 1100×850
- ✅ Try different grid size (4×4 smaller)
- ✅ Check display scaling settings

---

## Visualization Guide

### Color Coding

| Color                      | Meaning           | Algorithm    |
| -------------------------- | ----------------- | ------------ |
| 🔵 Dark Blue on Light Blue | Original clue     | Both         |
| 🟡 Yellow                  | Testing number    | Backtracking |
| 🔴 Red                     | Invalid/rejected  | Backtracking |
| 🟢 Green                   | Valid placement   | Backtracking |
| 🔴 Light Red               | Backtracking      | Backtracking |
| 🟠 Orange                  | Evolving solution | Cultural     |
| 🔵 Blue                    | Final solution    | Both         |

---

### Speed Controls

**Action Speed (1-500ms)**:

- Controls: Placement, Backtracking
- Recommended: 50ms

**Check Speed (10-1000ms)**:

- Controls: Number testing, Rejection
- Recommended: 100ms for clarity, 10ms for speed

---

## Tips & Best Practices

### For Best Results

1. **Use Backtracking for**:

   - Guaranteed solutions
   - Fast solving
   - Production use
   - Easy to hard puzzles

2. **Use Cultural Algorithm for**:

   - Learning about evolutionary algorithms
   - Watching solution evolution
   - Exploring alternative approaches
   - Educational demonstrations

3. **Visualization Tips**:

   - Start with easy puzzles to learn
   - Adjust speeds for comfort
   - Use Pause to examine interesting states
   - Try both algorithms on same puzzle

4. **Performance Tips**:
   - Disable visualization for speed
   - Use smaller grids (4×4) for testing
   - Close other applications during CA
   - Be patient with difficult puzzles

---

## Contributing

This project is developed for educational purposes. Code contributions should:

- Follow PEP 8 style guidelines
- Include docstrings for functions/classes
- Add comments for complex logic
- Test with multiple grid sizes

---

## License

Educational project for AI university course.

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Python**: 3.7+  
**Dependencies**: tkinter (standard library)
