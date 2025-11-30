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
    """
    Main GUI application for the Sudoku Solver.
    Provides interface for inputting puzzles, selecting algorithms,
    and visualizing the solving process.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        self.root = root
        self.root.title("🧩 Sudoku Puzzle Solver - AI Project")
        self.root.geometry("1200x900")  # Increased window size
        self.root.minsize(1100, 850)
        
        # Initialize styling system
        self.styles = SudokuStyles(root)
        
        self.size = 9  # Default grid size
        self.sudoku = None
        self.cells = {}
        self.original_values = set()  # Track pre-filled cells
        
        # Visualization state
        self.is_solving = False
        self.is_paused = False
        self.solving_thread = None
        self.visualization_speed = 50  # milliseconds delay for main actions
        self.attempt_speed = 100  # milliseconds delay for attempt/reject actions
        
        self._create_widgets()
        self._load_default_puzzle()
    
    def _create_widgets(self):
        """Create all GUI widgets and layout."""
        # Top control panel with gradient effect
        control_frame = ttk.Frame(self.root, style='Panel.TFrame', padding="15")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
        
        # Title
        title_label = ttk.Label(control_frame, text="🧩 Sudoku Puzzle Solver", 
                               style='Title.TLabel')
        title_label.pack(side=tk.TOP, pady=(0, 10))
        
        # Controls row
        controls_row = ttk.Frame(control_frame, style='Panel.TFrame')
        controls_row.pack(side=tk.TOP, fill=tk.X)
        
        # Grid size selection
        ttk.Label(controls_row, text="Grid Size:", style='Body.TLabel').pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="9x9")
        size_combo = ttk.Combobox(controls_row, textvariable=self.size_var, 
                                   values=["4x4", "6x6", "9x9"], state="readonly", width=10)
        size_combo.pack(side=tk.LEFT, padx=5)
        size_combo.bind("<<ComboboxSelected>>", self._on_size_change)
        
        # Sample puzzle selection
        ttk.Label(controls_row, text="Sample:", style='Body.TLabel').pack(side=tk.LEFT, padx=(20, 5))
        self.sample_var = tk.StringVar()
        self.sample_combo = ttk.Combobox(controls_row, textvariable=self.sample_var,
                                         state="readonly", width=18)
        self.sample_combo.pack(side=tk.LEFT, padx=5)
        self.sample_combo.bind("<<ComboboxSelected>>", self._load_sample)
        
        # Action buttons
        ttk.Button(controls_row, text="🎲 Generate Random", 
                   command=self._generate_puzzle,
                   style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_row, text="🗑️ Clear", 
                   command=self._clear_grid,
                   style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Main content frame
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Grid frame (left side) with shadow effect
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
        
        # Control panel (right side)
        right_panel = ttk.Frame(main_frame, style='Panel.TFrame', padding="15")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Algorithm selection card
        algo_frame = ttk.LabelFrame(right_panel, text="⚙️ Algorithm Selection", 
                                    style='Card.TLabelframe', padding="15")
        algo_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.algorithm_var = tk.StringVar(value="backtracking")
        ttk.Radiobutton(algo_frame, text="🔄 Backtracking Algorithm", 
                        variable=self.algorithm_var, 
                        value="backtracking").pack(anchor=tk.W, pady=3)
        ttk.Radiobutton(algo_frame, text="🧬 Cultural Algorithm", 
                        variable=self.algorithm_var, 
                        value="cultural").pack(anchor=tk.W, pady=3)
        
        # Visualization controls card
        viz_frame = ttk.LabelFrame(right_panel, text="🎬 Visualization Controls", 
                                   style='Card.TLabelframe', padding="15")
        viz_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Visualization checkbox
        self.visualize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(viz_frame, text="✨ Enable Step-by-Step Visualization", 
                        variable=self.visualize_var).pack(anchor=tk.W, pady=5)
        
        # Speed controls with better styling
        speed_container = ttk.Frame(viz_frame, style='Panel.TFrame')
        speed_container.pack(fill=tk.X, pady=5)
        
        # Action speed
        ttk.Label(speed_container, text="⚡ Action Speed:", 
                 style='Body.TLabel', width=14).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=5)
        self.speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(speed_container, from_=1, to=500, orient=tk.HORIZONTAL,
                               variable=self.speed_var, command=self._on_speed_change)
        speed_scale.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.speed_label = ttk.Label(speed_container, text="50ms", 
                                     style='Body.TLabel', width=8)
        self.speed_label.grid(row=0, column=2, sticky='e', pady=5)
        
        # Check speed
        ttk.Label(speed_container, text="🔍 Check Speed:", 
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
        
        # Speed hint
        hint_text = "💡 Action: placement & backtracking | Check: testing numbers"
        hint_label = ttk.Label(viz_frame, text=hint_text, style='Hint.TLabel')
        hint_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(right_panel, style='Panel.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.solve_button = ttk.Button(button_frame, text="▶️ Solve Puzzle", 
                                       command=self._solve_puzzle,
                                       style='Accent.TButton')
        self.solve_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.pause_button = ttk.Button(button_frame, text="⏸️ Pause", 
                                       command=self._toggle_pause,
                                       style='Secondary.TButton',
                                       state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                      command=self._stop_solving,
                                      style='Secondary.TButton',
                                      state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Metrics display card
        metrics_frame = ttk.LabelFrame(right_panel, text="📊 Performance Metrics", 
                                      style='Card.TLabelframe', padding="15")
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.metrics_text = tk.Text(metrics_frame, height=10, width=35, 
                                     state=tk.DISABLED, wrap=tk.WORD)
        self.styles.create_text_widget_style(self.metrics_text)
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="✅ Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var)
        self.styles.create_status_bar_style(status_bar)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5, 10))
        
        self._create_grid()
    
    def _on_speed_change(self, value):
        """Update speed label and main visualization speed."""
        speed = int(float(value))
        self.speed_label.config(text=f"{speed}ms")
        self.visualization_speed = speed
    
    def _on_attempt_speed_change(self, value):
        """Update attempt speed label and attempt visualization speed."""
        speed = int(float(value))
        self.attempt_speed_label.config(text=f"{speed}ms")
        self.attempt_speed = speed
    
    def _toggle_pause(self):
        """Toggle pause state during solving."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Resume")
            self.status_var.set("Paused")
        else:
            self.pause_button.config(text="Pause")
            self.status_var.set("Solving...")
    
    def _stop_solving(self):
        """Stop the solving process."""
        self.is_solving = False
        self.is_paused = False
        self._enable_controls()
        self.status_var.set("Stopped")
    
    def _enable_controls(self):
        """Enable input controls after solving."""
        self.solve_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Pause")
        self.stop_button.config(state=tk.DISABLED)
    
    def _disable_controls(self):
        """Disable input controls during solving."""
        self.solve_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
    
    def _create_grid(self):
        """Create the Sudoku grid of entry cells with enhanced styling and subtle box borders."""
        # Clear existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.cells = {}
        box_size = int(self.size ** 0.5)
        # Increased cell width for better visibility
        cell_width = 4 if self.size == 4 else (4 if self.size == 6 else 3)
        
        for row in range(self.size):
            for col in range(self.size):
                # Determine border thickness based on position in grid
                # Slightly thicker borders for box boundaries (2px instead of 3px)
                border_width_left = 2 if col % box_size == 0 else 0
                border_width_top = 2 if row % box_size == 0 else 0
                border_width_right = 2 if (col + 1) % box_size == 0 or col == self.size - 1 else 1
                border_width_bottom = 2 if (row + 1) % box_size == 0 or row == self.size - 1 else 1
                
                # Create a frame for each cell to handle borders
                cell_frame = tk.Frame(self.grid_frame, 
                                     bg='#2c3e50',  # Subtle dark border color
                                     highlightthickness=0)
                cell_frame.grid(row=row, column=col, sticky='nsew')
                
                # Configure row and column weights for proper sizing
                cell_frame.grid_rowconfigure(0, weight=1)
                cell_frame.grid_columnconfigure(0, weight=1)
                
                # Add padding to create border effect
                padx_left = border_width_left
                padx_right = border_width_right
                pady_top = border_width_top
                pady_bottom = border_width_bottom
                
                cell = tk.Entry(cell_frame, width=cell_width, justify=tk.CENTER,
                               borderwidth=0, highlightthickness=0)
                self.styles.create_cell_style(cell, state='normal', is_fixed=False)
                
                # Pack with padding to create border effect
                cell.pack(padx=(padx_left, padx_right), pady=(pady_top, pady_bottom), 
                         fill=tk.BOTH, expand=True, ipadx=8, ipady=8)  # Added internal padding
                
                # Validate input to allow only numbers
                cell.bind("<KeyRelease>", lambda e, r=row, c=col: self._validate_input(r, c))
                
                self.cells[(row, col)] = cell
    
    def _validate_input(self, row, col):
        """
        Validate user input in a cell.
        
        Args:
            row (int): Cell row
            col (int): Cell column
        """
        cell = self.cells[(row, col)]
        value = cell.get().strip()
        
        if value and (not value.isdigit() or int(value) < 1 or int(value) > self.size):
            cell.delete(0, tk.END)
    
    def _on_size_change(self, event=None):
        """Handle grid size change."""
        size_str = self.size_var.get()
        self.size = int(size_str.split('x')[0])
        self._create_grid()
        self._update_sample_list()
        self._clear_grid()
    
    def _update_sample_list(self):
        """Update the sample puzzle dropdown based on current size."""
        samples = PuzzleGenerator.get_sample_puzzles()
        matching_samples = [name for name in samples.keys() 
                           if name.startswith(f"{self.size}x{self.size}")]
        self.sample_combo['values'] = matching_samples
        if matching_samples:
            self.sample_combo.set(matching_samples[0])
    
    def _load_default_puzzle(self):
        """Load a default sample puzzle."""
        self._update_sample_list()
        self._load_sample()
    
    def _load_sample(self, event=None):
        """Load selected sample puzzle into the grid."""
        sample_name = self.sample_var.get()
        if not sample_name:
            return
        
        samples = PuzzleGenerator.get_sample_puzzles()
        if sample_name in samples:
            sudoku = samples[sample_name]
            self._display_puzzle(sudoku)
    
    def _generate_puzzle(self):
        """Generate a random puzzle."""
        difficulty = 'medium'
        sudoku = PuzzleGenerator.generate(self.size, difficulty)
        self._display_puzzle(sudoku)
        self.status_var.set(f"Generated {self.size}x{self.size} {difficulty} puzzle")
    
    def _display_puzzle(self, sudoku):
        """Display a puzzle in the grid with enhanced styling."""
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
        """Clear all cells in the grid."""
        for cell in self.cells.values():
            cell.config(state=tk.NORMAL, bg="white", fg="black")
            cell.delete(0, tk.END)
        
        self.original_values = set()
        self.sudoku = None
        self._clear_metrics()
        self.status_var.set("Grid cleared")
    
    def _get_current_puzzle(self):
        """
        Get the current puzzle from the grid.
        
        Returns:
            Sudoku: Current puzzle state
        """
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        for row in range(self.size):
            for col in range(self.size):
                value = self.cells[(row, col)].get().strip()
                if value.isdigit():
                    grid[row][col] = int(value)
        
        return Sudoku(self.size, grid)
    
    def _solve_puzzle(self):
        """Solve the current puzzle using selected algorithm."""
        if self.is_solving:
            return
        
        # Get current puzzle
        puzzle = self._get_current_puzzle()
        
        # Check if puzzle has any values
        if puzzle.is_complete():
            messagebox.showinfo("Info", "Puzzle is already complete!")
            return
        
        algorithm = self.algorithm_var.get()
        visualize = self.visualize_var.get()
        
        self.is_solving = True
        self.is_paused = False
        
        if visualize:
            self._disable_controls()
            # Run solving in separate thread to keep GUI responsive
            self.solving_thread = threading.Thread(
                target=self._solve_with_visualization,
                args=(puzzle, algorithm),
                daemon=True
            )
            self.solving_thread.start()
        else:
            # Solve without visualization (fast)
            self._solve_without_visualization(puzzle, algorithm)
    
    def _solve_without_visualization(self, puzzle, algorithm):
        """Solve puzzle instantly without visualization."""
        self.status_var.set(f"Solving with {algorithm}...")
        self.root.update()
        
        start_time = time.time()
        
        try:
            if algorithm == "backtracking":
                solver = BacktrackingSolver(puzzle)
                success = solver.solve(collect_steps=False)
            else:  # cultural
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
        """Solve puzzle with step-by-step visualization."""
        start_time = time.time()
        
        try:
            if algorithm == "backtracking":
                self._solve_backtracking_visualized(puzzle)
            else:  # cultural
                self._solve_cultural_visualized(puzzle)
            
            elapsed_time = time.time() - start_time
            
            if self.is_solving:  # Not stopped by user
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
        """Solve with backtracking and visualize each step."""
        solver = BacktrackingSolver(puzzle)
        
        step_count = [0]
        start_time = time.time()
        
        def visualization_callback(action, row, col, value, grid):
            if not self.is_solving:
                return False  # Stop solving
            
            # Wait if paused
            while self.is_paused and self.is_solving:
                time.sleep(0.1)
            
            if not self.is_solving:
                return False
            
            step_count[0] += 1
            
            # Update GUI in main thread with appropriate action
            self.root.after(0, self._update_cell_visualization, row, col, value, action)
            
            # Update metrics periodically
            if step_count[0] % 5 == 0:  # Update more frequently to show attempts
                elapsed = time.time() - start_time
                metrics = {
                    'algorithm': 'Backtracking',
                    'iterations': step_count[0],
                    'backtracks': solver.backtrack_count,
                    'time': elapsed
                }
                self.root.after(0, self._display_metrics, metrics)
            
            # Different delays based on action type with independent speed controls
            if action == 'attempt':
                # Use attempt speed for checking numbers
                time.sleep(self.attempt_speed / 1000.0)
            elif action == 'reject':
                # Use attempt speed for rejected numbers
                time.sleep(self.attempt_speed / 1000.0)
            elif action == 'place':
                # Use main speed for successful placement
                time.sleep(self.visualization_speed / 1000.0)
            elif action == 'backtrack':
                # Use main speed for backtracking
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
        """Solve with Cultural Algorithm and visualize each generation."""
        solver = CulturalAlgorithmSolver(puzzle, population_size=100, max_generations=1000)
        
        start_time = time.time()
        best_solution = [None]  # Store best solution in list to modify from callback
        last_fitness = [float('inf')]  # Track if fitness is improving
        stuck_count = [0]  # Count generations without improvement
        
        def visualization_callback(generation, best_grid, best_fitness):
            if not self.is_solving:
                return False
            
            # Wait if paused
            while self.is_paused and self.is_solving:
                time.sleep(0.1)
            
            if not self.is_solving:
                return False
            
            # Check if stuck (no improvement)
            if best_fitness >= last_fitness[0]:
                stuck_count[0] += 1
            else:
                stuck_count[0] = 0
                last_fitness[0] = best_fitness
            
            # Store best solution
            best_solution[0] = best_grid
            
            # Update grid only every few generations to reduce visual noise
            update_frequency = 1 if generation < 50 else (5 if generation < 200 else 10)
            if generation % update_frequency == 0 or best_fitness == 0:
                self.root.after(0, self._display_solution_partial, best_grid)
            
            # Update metrics
            elapsed = time.time() - start_time
            metrics = {
                'algorithm': 'Cultural Algorithm',
                'iterations': generation,
                'best_fitness': best_fitness,
                'time': elapsed
            }
            self.root.after(0, self._display_metrics, metrics)
            
            # Update status with more info
            status_msg = f"Gen {generation}, Fitness: {best_fitness}"
            if stuck_count[0] > 20:
                status_msg += " (searching for better solution...)"
            self.root.after(0, lambda: self.status_var.set(status_msg))
            
            # Adaptive delay - slower at start, faster later
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
            # Get the actual solution from solver
            solution = solver.get_solution()
            if solution:
                elapsed = time.time() - start_time
                metrics = solver.get_metrics()
                metrics['time'] = elapsed
                
                self.root.after(0, self._display_solution, solution)
                self.root.after(0, self._display_metrics, metrics)
                
                # Show result message
                if success:
                    self.root.after(0, lambda: self.status_var.set("✅ Solved!"))
                else:
                    self.root.after(0, lambda: self.status_var.set(
                        f"⚠️ Best fitness: {metrics['best_fitness']} (not fully solved)"))

    def _update_cell_visualization(self, row, col, value, action):
        """Update a single cell during visualization with enhanced color coding."""
        if (row, col) not in self.original_values:
            cell = self.cells[(row, col)]
            cell.delete(0, tk.END)
            
            if value != 0:
                cell.insert(0, str(value))
            
            # Map action to style state
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
        """Display partial solution during Cultural Algorithm with styling."""
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.original_values:
                    cell = self.cells[(row, col)]
                    cell.delete(0, tk.END)
                    cell.insert(0, str(grid[row][col]))
                    self.styles.create_cell_style(cell, state='cultural', is_fixed=False)
        self.root.update_idletasks()
    
    def _display_solution(self, solution):
        """Display the final solution in the grid with styling."""
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.original_values:
                    cell = self.cells[(row, col)]
                    cell.delete(0, tk.END)
                    cell.insert(0, str(solution[row][col]))
                    self.styles.create_cell_style(cell, state='solution', is_fixed=False)
    
    def _display_metrics(self, metrics):
        """
        Display performance metrics.
        
        Args:
            metrics (dict): Dictionary of metrics
        """
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
        """Clear the metrics display."""
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.config(state=tk.DISABLED)

def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
