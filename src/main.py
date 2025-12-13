"""
Sudoku Puzzle Solver - Main Entry Point

This application provides an intelligent Sudoku solver using two algorithms:
1. Backtracking Algorithm - A systematic constraint satisfaction approach
2. Cultural Algorithm - An evolutionary computation technique

The GUI allows users to input puzzles, select algorithms, and visualize solutions.
"""
## this is comment
from gui.gui import main as gui_main

def main():
    """Launch the Sudoku Solver GUI application."""
    gui_main()

if __name__ == "__main__":
    main()
