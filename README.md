# Sudoku Puzzle Solver

An intelligent Sudoku puzzle solver featuring two distinct algorithms: **Backtracking** and **Cultural Algorithm**. Built with Python and Tkinter, this application provides an interactive GUI for solving Sudoku puzzles of various sizes and difficulties.

## Features

✨ **Dual Algorithm Support**

- **Backtracking Algorithm**: Fast, guaranteed solution using depth-first search
- **Cultural Algorithm**: Evolutionary approach with population and belief spaces

🎮 **Interactive GUI**

- Visual grid with sub-box highlighting
- Manual puzzle input or sample puzzle selection
- Random puzzle generation with difficulty levels
- Step-by-step visualization option
- Real-time performance metrics

📊 **Multiple Grid Sizes**

- 4x4 (2x2 sub-boxes)
- 9x9 (3x3 sub-boxes)
- Extensible to larger sizes

📈 **Performance Tracking**

- Iteration/generation count
- Backtrack statistics
- Execution time measurement
- Algorithm comparison

## Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Sudoku-Puzzle-Solver.git
cd Sudoku-Puzzle-Solver
```

2. Run the application:

```bash
python run.py
```

## Usage

### Starting the Application

```bash
python run.py
```

### Solving a Puzzle

1. **Input Method** (choose one):

   - Manually enter numbers in the grid
   - Select a sample puzzle from the dropdown
   - Generate a random puzzle

2. **Select Algorithm**:

   - Choose between Backtracking or Cultural Algorithm
   - Enable visualization for step-by-step solving (Backtracking only)

3. **Solve**:
   - Click "Solve Puzzle"
   - View the solution (shown in blue)
   - Check performance metrics in the right panel

### Controls

- **Grid Size**: Switch between 4x4 and 9x9 grids
- **Sample**: Load predefined puzzles
- **Generate Random**: Create a new random puzzle
- **Clear**: Reset the grid
- **Solve Puzzle**: Run the selected algorithm

## Project Structure
