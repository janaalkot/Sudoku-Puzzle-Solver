"""
Cultural Algorithm Sudoku Solver

This module provides a Cultural Algorithm-based solver for Sudoku puzzles.
The Cultural Algorithm maintains a population of candidate solutions and a 
belief space that accumulates knowledge about good solutions. This information 
is used to guide the search for solving the Sudoku puzzle.

Classes:
- CulturalAlgorithmSolver: The main solver class

Usage:
1. Create a Sudoku object with the puzzle to be solved.
2. Instantiate the CulturalAlgorithmSolver with the Sudoku object.
3. Call the `solve` method on the solver instance.
4. Retrieve the solution from the Sudoku object or directly from the solver.

Example:
    from models.sudoku import Sudoku
    from algorithms.cultural import CulturalAlgorithmSolver

    # Define your Sudoku puzzle (0s for empty cells)
    puzzle = Sudoku([
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

    # Create the solver
    solver = CulturalAlgorithmSolver(puzzle)

    # Solve the puzzle
    if solver.solve():
        print("Solved successfully!")
        print(solver.get_solution())
    else:
        print("Failed to solve.")
"""

import random
import copy
from models.sudoku import Sudoku

class CulturalAlgorithmSolver:
    """
    Solves Sudoku puzzles using a Cultural Algorithm approach.
    Maintains both a population space (candidate solutions) and 
    belief space (accumulated knowledge) to guide the search.
    """
    
    def __init__(self, sudoku, population_size=50, max_generations=1000):
        """
        Initialize the Cultural Algorithm solver.
        
        Args:
            sudoku (Sudoku): The Sudoku puzzle to solve
            population_size (int): Number of individuals in population
            max_generations (int): Maximum number of generations to run
        """
        self.original = sudoku.copy()
        self.size = sudoku.size
        self.population_size = population_size
        self.max_generations = max_generations
        self.fixed_cells = self._get_fixed_cells(sudoku)
        
        # Belief space: stores knowledge about good values for positions
        self.belief_space = self._initialize_belief_space()
        
        self.iterations = 0
        self.best_fitness = float('inf')
        self.steps = []
        self.visualization_callback = None
    
    def _get_fixed_cells(self, sudoku):
        """
        Identify cells that are pre-filled (fixed).
        
        Args:
            sudoku (Sudoku): The puzzle
            
        Returns:
            set: Set of (row, col) tuples for fixed cells
        """
        fixed = set()
        for row in range(sudoku.size):
            for col in range(sudoku.size):
                if sudoku.grid[row][col] != 0:
                    fixed.add((row, col))
        return fixed
    
    def _initialize_belief_space(self):
        """
        Initialize the belief space with possible values for each cell.
        
        Returns:
            dict: Belief space mapping (row, col) to list of possible values
        """
        belief = {}
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    belief[(row, col)] = self.original.get_possible_values(row, col)
                    if not belief[(row, col)]:
                        # If no valid values found, allow all
                        belief[(row, col)] = list(range(1, self.size + 1))
        return belief
    
    def _create_individual(self):
        """
        Create a random individual (candidate solution) using belief space.
        Uses row-permutation initialization for better validity.
        
        Returns:
            Sudoku: A candidate solution
        """
        individual = self.original.copy()
        
        # Fill each row with a permutation of remaining values
        for row in range(self.size):
            # Get already placed values in this row
            present = set(v for v in individual.grid[row] if v != 0)
            missing = [v for v in range(1, self.size + 1) if v not in present]
            random.shuffle(missing)
            
            # Fill empty cells in this row
            missing_idx = 0
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    if missing_idx < len(missing):
                        individual.grid[row][col] = missing[missing_idx]
                        missing_idx += 1
                    else:
                        # Fallback to random value
                        individual.grid[row][col] = random.randint(1, self.size)
        
        return individual
    
    def _fitness(self, individual):
        """
        Calculate fitness of an individual (lower is better).
        Fitness = number of constraint violations.
        
        Args:
            individual (Sudoku): Candidate solution
            
        Returns:
            int: Fitness score (0 means solved)
        """
        violations = 0
        
        # Check rows for duplicates
        for row in range(self.size):
            seen = {}
            for col in range(self.size):
                val = individual.grid[row][col]
                if val != 0:
                    if val in seen:
                        violations += 1
                    seen[val] = True
        
        # Check columns for duplicates
        for col in range(self.size):
            seen = {}
            for row in range(self.size):
                val = individual.grid[row][col]
                if val != 0:
                    if val in seen:
                        violations += 1
                    seen[val] = True
        
        # Check boxes for duplicates
        box_size = individual.box_size
        for box_row in range(0, self.size, box_size):
            for box_col in range(0, self.size, box_size):
                seen = {}
                for r in range(box_row, box_row + box_size):
                    for c in range(box_col, box_col + box_size):
                        val = individual.grid[r][c]
                        if val != 0:
                            if val in seen:
                                violations += 1
                            seen[val] = True
        
        return violations
    
    def _crossover(self, parent1, parent2):
        """
        Perform crossover between two parents to create offspring.
        Uses row-based crossover to maintain better structure.
        
        Args:
            parent1 (Sudoku): First parent
            parent2 (Sudoku): Second parent
            
        Returns:
            Sudoku: Offspring
        """
        child = self.original.copy()
        
        # Row-based crossover: randomly choose rows from either parent
        for row in range(self.size):
            source = parent1 if random.random() < 0.5 else parent2
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    child.grid[row][col] = source.grid[row][col]
        
        return child
    
    def _mutate(self, individual, mutation_rate=0.15):
        """
        Mutate an individual by swapping values within rows.
        This preserves row validity better.
        
        Args:
            individual (Sudoku): Individual to mutate
            mutation_rate (float): Probability of mutating each row
        """
        for row in range(self.size):
            if random.random() < mutation_rate:
                # Find non-fixed cells in this row
                indices = [col for col in range(self.size) if (row, col) not in self.fixed_cells]
                if len(indices) >= 2:
                    # Swap two random non-fixed cells in the row
                    a, b = random.sample(indices, 2)
                    individual.grid[row][a], individual.grid[row][b] = \
                        individual.grid[row][b], individual.grid[row][a]
    
    def _update_belief_space(self, population):
        """
        Update belief space based on best individuals in population.
        
        Args:
            population (list): List of (individual, fitness) tuples
        """
        # Sort population by fitness (best first)
        population.sort(key=lambda x: x[1])
        
        # Use top 20% to update beliefs
        elite_count = max(1, len(population) // 5)
        elite = [ind for ind, fit in population[:elite_count]]
        
        # Update belief space with values from elite individuals
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    values = [ind.grid[row][col] for ind in elite]
                    # Keep values that appear frequently in elite
                    value_counts = {}
                    for v in values:
                        value_counts[v] = value_counts.get(v, 0) + 1
                    
                    # Update belief space with most common values
                    good_values = [v for v, count in value_counts.items() 
                                   if count >= elite_count * 0.3]
                    if good_values:
                        self.belief_space[(row, col)] = good_values
    
    def solve(self, collect_steps=False, callback=None):
        """
        Solve the puzzle using Cultural Algorithm.
        
        Args:
            collect_steps (bool): Whether to collect steps for visualization
            callback (callable): Optional callback function(generation, best_grid, best_fitness)
                                called after each generation for visualization
            
        Returns:
            bool: True if solved, False otherwise
        """
        self.visualization_callback = callback
        
        # Initialize population
        population = []
        for _ in range(self.population_size):
            individual = self._create_individual()
            fitness = self._fitness(individual)
            population.append((individual, fitness))
        
        self.iterations = 0
        self.best_solution = None  # Store the best solution found
        
        for generation in range(self.max_generations):
            self.iterations = generation + 1
            
            # Find best in current population
            population.sort(key=lambda x: x[1])
            best_individual, best_fitness = population[0]
            self.best_fitness = best_fitness
            
            # Store best solution
            if self.best_solution is None or best_fitness < self._fitness(self.best_solution):
                self.best_solution = best_individual.copy()
            
            # Visualization callback for each generation
            if self.visualization_callback:
                import copy as cp
                # Check if callback returns False (stop signal)
                result = self.visualization_callback(
                    generation + 1, 
                    cp.deepcopy(best_individual.grid), 
                    best_fitness
                )
                if result is False:
                    break
            
            # Check if solved
            if best_fitness == 0:
                self.best_solution = best_individual.copy()
                return True
            
            # Update belief space
            self._update_belief_space(population)
            
            # Create new population
            new_population = []
            
            # Elitism: keep best individuals
            elite_count = max(2, self.population_size // 10)
            new_population.extend(population[:elite_count])
            
            # Generate offspring
            while len(new_population) < self.population_size:
                # Tournament selection
                tournament_size = min(3, len(population))
                parent1 = min(random.sample(population, tournament_size), key=lambda x: x[1])[0]
                parent2 = min(random.sample(population, tournament_size), key=lambda x: x[1])[0]
                
                # Crossover
                child = self._crossover(parent1, parent2)
                
                # Mutation
                self._mutate(child)
                
                # Evaluate
                fitness = self._fitness(child)
                new_population.append((child, fitness))
            
            population = new_population
            
            # Random restart if stuck (every 200 generations)
            if generation % 200 == 0 and generation > 0:
                # Check if we're making progress
                avg_fitness = sum(f for _, f in population) / len(population)
                if avg_fitness > best_fitness * 2:  # If average is much worse than best
                    # Replace worst half with new random individuals
                    for i in range(self.population_size // 2, self.population_size):
                        ind = self._create_individual()
                        population[i] = (ind, self._fitness(ind))
        
        # Return best solution found (even if not perfect)
        if self.best_solution is None:
            population.sort(key=lambda x: x[1])
            self.best_solution = population[0][0].copy()
        
        return self.best_fitness == 0
    
    def get_solution(self):
        """
        Get the best solution found.
        
        Returns:
            list: 2D list representing the solution
        """
        # Return the best solution stored during solving
        if hasattr(self, 'best_solution') and self.best_solution is not None:
            return self.best_solution.grid
        # Fallback: return original if no solution found
        return self.original.grid
    
    def get_metrics(self):
        """
        Get performance metrics.
        
        Returns:
            dict: Dictionary containing generation count and best fitness
        """
        return {
            'iterations': self.iterations,
            'best_fitness': self.best_fitness,
            'algorithm': 'Cultural Algorithm'
        }
