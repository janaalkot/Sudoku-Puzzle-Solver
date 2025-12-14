import random
import copy
from models.sudoku import Sudoku

class CulturalAlgorithmSolver:
    
    def __init__(self, sudoku, population_size=50, max_generations=1000):
        self.original = sudoku.copy()
        self.size = sudoku.size
        self.population_size = population_size
        self.max_generations = max_generations
        self.fixed_cells = self._get_fixed_cells(sudoku)
        self.belief_space = self._initialize_belief_space()
        self.iterations = 0
        self.best_fitness = float('inf')
        self.steps = []
        self.visualization_callback = None
    
    def _get_fixed_cells(self, sudoku):
        fixed = set()
        for row in range(sudoku.size):
            for col in range(sudoku.size):
                if sudoku.grid[row][col] != 0:
                    fixed.add((row, col))
        return fixed
    
    def _initialize_belief_space(self):
        belief = {}
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    belief[(row, col)] = self.original.get_possible_values(row, col)
                    if not belief[(row, col)]:
                        belief[(row, col)] = list(range(1, self.size + 1))
        return belief
    
    def _create_individual(self):
        individual = self.original.copy()
        
        for row in range(self.size):
            present = set(v for v in individual.grid[row] if v != 0)
            missing = [v for v in range(1, self.size + 1) if v not in present]
            random.shuffle(missing)
            
            missing_idx = 0
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    if missing_idx < len(missing):
                        individual.grid[row][col] = missing[missing_idx]
                        missing_idx += 1
                    else:
                        individual.grid[row][col] = random.randint(1, self.size)
        
        return individual
    
    def _fitness(self, individual):
        violations = 0
        
        for row in range(self.size):
            seen = {}
            for col in range(self.size):
                val = individual.grid[row][col]
                if val != 0:
                    if val in seen:
                        violations += 1
                    seen[val] = True
        
        for col in range(self.size):
            seen = {}
            for row in range(self.size):
                val = individual.grid[row][col]
                if val != 0:
                    if val in seen:
                        violations += 1
                    seen[val] = True
        
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
        child = self.original.copy()
        
        for row in range(self.size):
            source = parent1 if random.random() < 0.5 else parent2
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    child.grid[row][col] = source.grid[row][col]
        
        return child
    
    def _mutate(self, individual, mutation_rate=0.15):
        for row in range(self.size):
            if random.random() < mutation_rate:
                indices = [col for col in range(self.size) if (row, col) not in self.fixed_cells]
                if len(indices) >= 2:
                    a, b = random.sample(indices, 2)
                    individual.grid[row][a], individual.grid[row][b] = \
                        individual.grid[row][b], individual.grid[row][a]
    
    def _update_belief_space(self, population):
        population.sort(key=lambda x: x[1])
        
        elite_count = max(1, len(population) // 5)
        elite = [ind for ind, fit in population[:elite_count]]
        
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.fixed_cells:
                    values = [ind.grid[row][col] for ind in elite]
                    value_counts = {}
                    for v in values:
                        value_counts[v] = value_counts.get(v, 0) + 1
                    
                    good_values = [v for v, count in value_counts.items() 
                                   if count >= elite_count * 0.3]
                    if good_values:
                        self.belief_space[(row, col)] = good_values
    
    def solve(self, collect_steps=False, callback=None):
        self.visualization_callback = callback
        
        population = []
        for _ in range(self.population_size):
            individual = self._create_individual()
            fitness = self._fitness(individual)
            population.append((individual, fitness))
        
        self.iterations = 0
        self.best_solution = None
        
        for generation in range(self.max_generations):
            self.iterations = generation + 1
            
            population.sort(key=lambda x: x[1])
            best_individual, best_fitness = population[0]
            self.best_fitness = best_fitness
            
            if self.best_solution is None or best_fitness < self._fitness(self.best_solution):
                self.best_solution = best_individual.copy()
            
            if self.visualization_callback:
                import copy as cp
                result = self.visualization_callback(
                    generation + 1, 
                    cp.deepcopy(best_individual.grid), 
                    best_fitness
                )
                if result is False:
                    break
            
            if best_fitness == 0:
                self.best_solution = best_individual.copy()
                return True
            
            self._update_belief_space(population)
            
            new_population = []
            
            elite_count = max(2, self.population_size // 10)
            new_population.extend(population[:elite_count])
            
            while len(new_population) < self.population_size:
                tournament_size = min(3, len(population))
                parent1 = min(random.sample(population, tournament_size), key=lambda x: x[1])[0]
                parent2 = min(random.sample(population, tournament_size), key=lambda x: x[1])[0]
                
                child = self._crossover(parent1, parent2)
                
                self._mutate(child)
                
                fitness = self._fitness(child)
                new_population.append((child, fitness))
            
            population = new_population
            
            if generation % 200 == 0 and generation > 0:
                avg_fitness = sum(f for _, f in population) / len(population)
                if avg_fitness > best_fitness * 2:
                    for i in range(self.population_size // 2, self.population_size):
                        ind = self._create_individual()
                        population[i] = (ind, self._fitness(ind))
        
        if self.best_solution is None:
            population.sort(key=lambda x: x[1])
            self.best_solution = population[0][0].copy()
        
        return self.best_fitness == 0
    
    def get_solution(self):
        if hasattr(self, 'best_solution') and self.best_solution is not None:
            return self.best_solution.grid
        return self.original.grid
    
    def get_metrics(self):
        return {
            'iterations': self.iterations,
            'best_fitness': self.best_fitness,
            'algorithm': 'Cultural Algorithm'
        }
