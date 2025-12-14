import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from models.sudoku import Sudoku
from algorithms.backtracking import BacktrackingSolver
from algorithms.cultural import CulturalAlgorithmSolver
from utils.puzzle_generator import PuzzleGenerator
from gui.styles import SudokuStyles

class SudokuGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Puzzle Solver - AI Project")
        self.root.geometry("1200x900")
        self.root.minsize(1100, 850)
        
        self.styles = SudokuStyles(root)
        
        self.size = 9
        self.sudoku = None
        self.cells = {}
        self.original_values = set()
        
        self.is_solving = False
        self.is_paused = False
        self.solving_thread = None
        self.visualization_speed = 50
        self.attempt_speed = 100
        
        self._create_widgets()
        self._load_default_puzzle()
    
    def _create_widgets(self):
        control_frame = ttk.Frame(self.root, style='Panel.TFrame', padding="15")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
        
        title_label = ttk.Label(control_frame, text="Sudoku Puzzle Solver", 
                               style='Title.TLabel')
        title_label.pack(side=tk.TOP, pady=(0, 10))
        
        controls_row = ttk.Frame(control_frame, style='Panel.TFrame')
        controls_row.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Label(controls_row, text="Grid Size:", style='Body.TLabel').pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="9x9")
        size_combo = ttk.Combobox(controls_row, textvariable=self.size_var, 
                                   values=["4x4", "6x6", "9x9"], state="readonly", width=10)
        size_combo.pack(side=tk.LEFT, padx=5)
        size_combo.bind("<<ComboboxSelected>>", self._on_size_change)
        
        ttk.Label(controls_row, text="Sample:", style='Body.TLabel').pack(side=tk.LEFT, padx=(20, 5))
        self.sample_var = tk.StringVar()
        self.sample_combo = ttk.Combobox(controls_row, textvariable=self.sample_var,
                                         state="readonly", width=18)
        self.sample_combo.pack(side=tk.LEFT, padx=5)
        self.sample_combo.bind("<<ComboboxSelected>>", self._load_sample)
        
        ttk.Button(controls_row, text="Generate Random", 
                   command=self._generate_puzzle,
                   style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_row, text="Clear", 
                   command=self._clear_grid,
                   style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        grid_container = ttk.Frame(main_frame, style='Panel.TFrame', padding="10")
        grid_container.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.grid_frame = tk.Frame(grid_container, 
                                   bg=self.styles.COLORS['bg_grid'],
                                   relief='flat',
                                   borderwidth=3,
                                   highlightthickness=2,
                                   highlightbackground=self.styles.COLORS['border_accent'],
                                   highlightcolor=self.styles.COLORS['primary'])
        self.grid_frame.pack(padx=5, pady=5)
        
        right_panel = ttk.Frame(main_frame, style='Panel.TFrame', padding="15")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        algo_frame = ttk.LabelFrame(right_panel, text="Algorithm Selection", 
                                    style='Card.TLabelframe', padding="15")
        algo_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.algorithm_var = tk.StringVar(value="backtracking")
        ttk.Radiobutton(algo_frame, text="Backtracking Algorithm", 
                        variable=self.algorithm_var, 
                        value="backtracking").pack(anchor=tk.W, pady=3)
        ttk.Radiobutton(algo_frame, text="Cultural Algorithm", 
                        variable=self.algorithm_var, 
                        value="cultural").pack(anchor=tk.W, pady=3)
        
        viz_frame = ttk.LabelFrame(right_panel, text="Visualization Controls", 
                                   style='Card.TLabelframe', padding="15")
        viz_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.visualize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(viz_frame, text="Enable Step-by-Step Visualization", 
                        variable=self.visualize_var).pack(anchor=tk.W, pady=5)
        
        speed_container = ttk.Frame(viz_frame, style='Panel.TFrame')
        speed_container.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_container, text="Action Speed:", 
                 style='Body.TLabel', width=14).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=5)
        self.speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(speed_container, from_=1, to=500, orient=tk.HORIZONTAL,
                               variable=self.speed_var, command=self._on_speed_change)
        speed_scale.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.speed_label = ttk.Label(speed_container, text="50ms", 
                                     style='Body.TLabel', width=8)
        self.speed_label.grid(row=0, column=2, sticky='e', pady=5)
        
        ttk.Label(speed_container, text="Check Speed:", 
                 style='Body.TLabel', width=14).grid(row=1, column=0, sticky='w', padx=(0, 5), pady=5)
        self.attempt_speed_var = tk.IntVar(value=100)
        attempt_speed_scale = ttk.Scale(speed_container, from_=10, to=1000, 
                                       orient=tk.HORIZONTAL,
                                       variable=self.attempt_speed_var, 
                                       command=self._on_attempt_speed_change)
        attempt_speed_scale.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        self.attempt_speed_label = ttk.Label(speed_container, text="100ms", 
                                            style='Body.TLabel', width=8)
        self.attempt_speed_label.grid(row=1, column=2, sticky='e', pady=5)
        
        speed_container.columnconfigure(1, weight=1)
        
        hint_text = "Action: placement & backtracking | Check: testing numbers"
        hint_label = ttk.Label(viz_frame, text=hint_text, style='Hint.TLabel')
        hint_label.pack(anchor=tk.W, pady=(5, 0))
        
        button_frame = ttk.Frame(right_panel, style='Panel.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.solve_button = ttk.Button(button_frame, text="Solve Puzzle", 
                                       command=self._solve_puzzle,
                                       style='Accent.TButton')
        self.solve_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.pause_button = ttk.Button(button_frame, text="Pause", 
                                       command=self._toggle_pause,
                                       style='Secondary.TButton',
                                       state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                      command=self._stop_solving,
                                      style='Secondary.TButton',
                                      state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        metrics_frame = ttk.LabelFrame(right_panel, text="Performance Metrics", 
                                      style='Card.TLabelframe', padding="15")
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.metrics_text = tk.Text(metrics_frame, height=10, width=35, 
                                     state=tk.DISABLED, wrap=tk.WORD)
        self.styles.create_text_widget_style(self.metrics_text)
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var)
        self.styles.create_status_bar_style(status_bar)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5, 10))
        
        self._create_grid()
    
    def _on_speed_change(self, value):
        speed = int(float(value))
        self.speed_label.config(text=f"{speed}ms")
        self.visualization_speed = speed
    
    def _on_attempt_speed_change(self, value):
        speed = int(float(value))
        self.attempt_speed_label.config(text=f"{speed}ms")
        self.attempt_speed = speed
    
    def _toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Resume")
            self.status_var.set("Paused")
        else:
            self.pause_button.config(text="Pause")
            self.status_var.set("Solving...")
    
    def _stop_solving(self):
        self.is_solving = False
        self.is_paused = False
        self._enable_controls()
        self.status_var.set("Stopped")
    
    def _enable_controls(self):
        self.solve_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Pause")
        self.stop_button.config(state=tk.DISABLED)
    
    def _disable_controls(self):
        self.solve_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
    
    def _create_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.cells = {}
        box_size = int(self.size ** 0.5)
        cell_width = 4 if self.size == 4 else (4 if self.size == 6 else 3)
        
        for row in range(self.size):
            for col in range(self.size):
                border_width_left = 2 if col % box_size == 0 else 0
                border_width_top = 2 if row % box_size == 0 else 0
                border_width_right = 2 if (col + 1) % box_size == 0 or col == self.size - 1 else 1
                border_width_bottom = 2 if (row + 1) % box_size == 0 or row == self.size - 1 else 1
                
                cell_frame = tk.Frame(self.grid_frame, 
                                     bg='#2c3e50',
                                     highlightthickness=0)
                cell_frame.grid(row=row, column=col, sticky='nsew')
                
                cell_frame.grid_rowconfigure(0, weight=1)
                cell_frame.grid_columnconfigure(0, weight=1)
                
                padx_left = border_width_left
                padx_right = border_width_right
                pady_top = border_width_top
                pady_bottom = border_width_bottom
                
                cell = tk.Entry(cell_frame, width=cell_width, justify=tk.CENTER,
                               borderwidth=0, highlightthickness=0)
                self.styles.create_cell_style(cell, state='normal', is_fixed=False)
                
                cell.pack(padx=(padx_left, padx_right), pady=(pady_top, pady_bottom), 
                         fill=tk.BOTH, expand=True, ipadx=8, ipady=8)
                
                cell.bind("<KeyRelease>", lambda e, r=row, c=col: self._validate_input(r, c))
                
                self.cells[(row, col)] = cell
    
    def _validate_input(self, row, col):
        cell = self.cells[(row, col)]
        value = cell.get().strip()
        
        if value and (not value.isdigit() or int(value) < 1 or int(value) > self.size):
            cell.delete(0, tk.END)
    
    def _on_size_change(self, event=None):
        size_str = self.size_var.get()
        self.size = int(size_str.split('x')[0])
        self._create_grid()
        self._update_sample_list()
        self._clear_grid()
    
    def _update_sample_list(self):
        samples = PuzzleGenerator.get_sample_puzzles()
        matching_samples = [name for name in samples.keys() 
                           if name.startswith(f"{self.size}x{self.size}")]
        self.sample_combo['values'] = matching_samples
        if matching_samples:
            self.sample_combo.set(matching_samples[0])
    
    def _load_default_puzzle(self):
        self._update_sample_list()
        self._load_sample()
    
    def _load_sample(self, event=None):
        sample_name = self.sample_var.get()
        if not sample_name:
            return
        
        samples = PuzzleGenerator.get_sample_puzzles()
        if sample_name in samples:
            sudoku = samples[sample_name]
            self._display_puzzle(sudoku)
    
    def _generate_puzzle(self):
        difficulty = 'medium'
        sudoku = PuzzleGenerator.generate(self.size, difficulty)
        self._display_puzzle(sudoku)
        self.status_var.set(f"Generated {self.size}x{self.size} {difficulty} puzzle")
    
    def _display_puzzle(self, sudoku):
        self.sudoku = sudoku
        self.original_values = set()
        
        for row in range(self.size):
            for col in range(self.size):
                cell = self.cells[(row, col)]
                cell.config(state=tk.NORMAL)
                cell.delete(0, tk.END)
                
                value = sudoku.grid[row][col]
                if value != 0:
                    cell.insert(0, str(value))
                    self.styles.create_cell_style(cell, state='normal', is_fixed=True)
                    self.original_values.add((row, col))
                else:
                    self.styles.create_cell_style(cell, state='normal', is_fixed=False)
    
    def _clear_grid(self):
        for cell in self.cells.values():
            cell.config(state=tk.NORMAL, bg="white", fg="black")
            cell.delete(0, tk.END)
        
        self.original_values = set()
        self.sudoku = None
        self._clear_metrics()
        self.status_var.set("Grid cleared")
    
    def _get_current_puzzle(self):
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        for row in range(self.size):
            for col in range(self.size):
                value = self.cells[(row, col)].get().strip()
                if value.isdigit():
                    grid[row][col] = int(value)
        
        return Sudoku(self.size, grid)
    
    def _solve_puzzle(self):
        if self.is_solving:
            return
        
        puzzle = self._get_current_puzzle()
        
        if puzzle.is_complete():
            messagebox.showinfo("Info", "Puzzle is already complete!")
            return
        
        algorithm = self.algorithm_var.get()
        visualize = self.visualize_var.get()
        
        self.is_solving = True
        self.is_paused = False
        
        if visualize:
            self._disable_controls()
            self.solving_thread = threading.Thread(
                target=self._solve_with_visualization,
                args=(puzzle, algorithm),
                daemon=True
            )
            self.solving_thread.start()
        else:
            self._solve_without_visualization(puzzle, algorithm)
    
    def _solve_without_visualization(self, puzzle, algorithm):
        self.status_var.set(f"Solving with {algorithm}...")
        self.root.update()
        
        start_time = time.time()
        
        try:
            if algorithm == "backtracking":
                solver = BacktrackingSolver(puzzle)
                success = solver.solve(collect_steps=False)
            else:
                solver = CulturalAlgorithmSolver(puzzle)
                success = solver.solve()
            
            elapsed_time = time.time() - start_time
            
            if success:
                solution = solver.get_solution()
                self._display_solution(solution)
                
                metrics = solver.get_metrics()
                metrics['time'] = elapsed_time
                self._display_metrics(metrics)
                
                self.status_var.set("Puzzle solved successfully!")
                messagebox.showinfo("Success", "Puzzle solved!")
            else:
                self.status_var.set("Could not solve puzzle")
                messagebox.showwarning("Failed", "Could not find a solution")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred")
        
        self.is_solving = False
    
    def _solve_with_visualization(self, puzzle, algorithm):
        start_time = time.time()
        
        try:
            if algorithm == "backtracking":
                self._solve_backtracking_visualized(puzzle)
            else:
                self._solve_cultural_visualized(puzzle)
            
            elapsed_time = time.time() - start_time
            
            if self.is_solving:
                self.root.after(0, lambda: self.status_var.set("Puzzle solved!"))
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Puzzle solved in {elapsed_time:.2f} seconds!"))
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                f"An error occurred: {str(e)}"))
        
        finally:
            self.is_solving = False
            self.root.after(0, self._enable_controls)
    
    def _solve_backtracking_visualized(self, puzzle):
        solver = BacktrackingSolver(puzzle)
        
        step_count = [0]
        start_time = time.time()
        
        def visualization_callback(action, row, col, value, grid):
            if not self.is_solving:
                return False
            
            while self.is_paused and self.is_solving:
                time.sleep(0.1)
            
            if not self.is_solving:
                return False
            
            step_count[0] += 1
            
            self.root.after(0, self._update_cell_visualization, row, col, value, action)
            
            if step_count[0] % 5 == 0:
                elapsed = time.time() - start_time
                metrics = {
                    'algorithm': 'Backtracking',
                    'iterations': step_count[0],
                    'backtracks': solver.backtrack_count,
                    'time': elapsed
                }
                self.root.after(0, self._display_metrics, metrics)
            
            if action == 'attempt':
                time.sleep(self.attempt_speed / 1000.0)
            elif action == 'reject':
                time.sleep(self.attempt_speed / 1000.0)
            elif action == 'place':
                time.sleep(self.visualization_speed / 1000.0)
            elif action == 'backtrack':
                time.sleep(self.visualization_speed / 1000.0)
            
            return self.is_solving
        
        self.root.after(0, lambda: self.status_var.set("Solving with Backtracking..."))
        success = solver.solve(collect_steps=True, callback=visualization_callback)
        
        if success and self.is_solving:
            solution = solver.get_solution()
            elapsed = time.time() - start_time
            metrics = solver.get_metrics()
            metrics['time'] = elapsed
            
            self.root.after(0, self._display_solution, solution)
            self.root.after(0, self._display_metrics, metrics)
    
    def _solve_cultural_visualized(self, puzzle):
        solver = CulturalAlgorithmSolver(puzzle, population_size=100, max_generations=1000)
        
        start_time = time.time()
        best_solution = [None]
        last_fitness = [float('inf')]
        stuck_count = [0]
        
        def visualization_callback(generation, best_grid, best_fitness):
            if not self.is_solving:
                return False
            
            while self.is_paused and self.is_solving:
                time.sleep(0.1)
            
            if not self.is_solving:
                return False
            
            if best_fitness >= last_fitness[0]:
                stuck_count[0] += 1
            else:
                stuck_count[0] = 0
                last_fitness[0] = best_fitness
            
            best_solution[0] = best_grid
            
            update_frequency = 1 if generation < 50 else (5 if generation < 200 else 10)
            if generation % update_frequency == 0 or best_fitness == 0:
                self.root.after(0, self._display_solution_partial, best_grid)
            
            elapsed = time.time() - start_time
            metrics = {
                'algorithm': 'Cultural Algorithm',
                'iterations': generation,
                'best_fitness': best_fitness,
                'time': elapsed
            }
            self.root.after(0, self._display_metrics, metrics)
            
            status_msg = f"Gen {generation}, Fitness: {best_fitness}"
            if stuck_count[0] > 20:
                status_msg += " (searching for better solution...)"
            self.root.after(0, lambda: self.status_var.set(status_msg))
            
            if generation < 50:
                delay = self.visualization_speed / 1000.0 * 3
            elif generation < 200:
                delay = self.visualization_speed / 1000.0 * 2
            else:
                delay = self.visualization_speed / 1000.0
            
            time.sleep(delay)
            
            return self.is_solving
        
        self.root.after(0, lambda: self.status_var.set("Solving with Cultural Algorithm..."))
        success = solver.solve(collect_steps=True, callback=visualization_callback)
        
        if self.is_solving:
            solution = solver.get_solution()
            if solution:
                elapsed = time.time() - start_time
                metrics = solver.get_metrics()
                metrics['time'] = elapsed
                
                self.root.after(0, self._display_solution, solution)
                self.root.after(0, self._display_metrics, metrics)
                
                if success:
                    self.root.after(0, lambda: self.status_var.set("Solved!"))
                else:
                    self.root.after(0, lambda: self.status_var.set(
                        f"Best fitness: {metrics['best_fitness']} (not fully solved)"))

    def _update_cell_visualization(self, row, col, value, action):
        if (row, col) not in self.original_values:
            cell = self.cells[(row, col)]
            cell.delete(0, tk.END)
            
            if value != 0:
                cell.insert(0, str(value))
            
            state_map = {
                'attempt': 'attempt',
                'reject': 'reject',
                'place': 'place',
                'backtrack': 'backtrack'
            }
            
            state = state_map.get(action, 'normal')
            self.styles.create_cell_style(cell, state=state, is_fixed=False)
            
            self.root.update_idletasks()
    
    def _display_solution_partial(self, grid):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.original_values:
                    cell = self.cells[(row, col)]
                    cell.delete(0, tk.END)
                    cell.insert(0, str(grid[row][col]))
                    self.styles.create_cell_style(cell, state='cultural', is_fixed=False)
        self.root.update_idletasks()
    
    def _display_solution(self, solution):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.original_values:
                    cell = self.cells[(row, col)]
                    cell.delete(0, tk.END)
                    cell.insert(0, str(solution[row][col]))
                    self.styles.create_cell_style(cell, state='solution', is_fixed=False)
    
    def _display_metrics(self, metrics):
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        
        text = f"Algorithm: {metrics['algorithm']}\n\n"
        text += f"Iterations: {metrics['iterations']}\n"
        
        if 'backtracks' in metrics:
            text += f"Backtracks: {metrics['backtracks']}\n"
        
        if 'best_fitness' in metrics:
            text += f"Best Fitness: {metrics['best_fitness']}\n"
        
        if 'time' in metrics:
            text += f"\nTime: {metrics['time']:.3f} seconds"
        
        self.metrics_text.insert(1.0, text)
        self.metrics_text.config(state=tk.DISABLED)
    
    def _clear_metrics(self):
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
