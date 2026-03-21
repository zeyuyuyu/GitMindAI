import numpy as np

class DifferentialEvolution:
    def __init__(self, obj_func, bounds, pop_size=50, F=0.8, CR=0.7, max_iter=1000):
        """
        Initialize Differential Evolution optimizer
        
        Args:
            obj_func: Objective function to minimize
            bounds: List of tuples (min, max) for each dimension
            pop_size: Population size
            F: Mutation factor (0,2)
            CR: Crossover rate (0,1) 
            max_iter: Maximum iterations
        """
        self.obj_func = obj_func
        self.bounds = np.array(bounds)
        self.pop_size = pop_size
        self.F = F
        self.CR = CR
        self.max_iter = max_iter
        self.dim = len(bounds)
        
    def init_population(self):
        """Initialize random population within bounds"""
        population = np.random.rand(self.pop_size, self.dim)
        min_b, max_b = self.bounds.T
        diff = np.fabs(min_b - max_b)
        population = min_b + population * diff
        return population
    
    def mutation(self, population):
        """Apply mutation using current-to-best/1 strategy"""
        pop_mut = np.zeros_like(population)
        
        for i in range(self.pop_size):
            # Select 3 random vectors
            idxs = [idx for idx in range(self.pop_size) if idx != i]
            a, b, c = population[np.random.choice(idxs, 3, replace=False)]
            
            # Mutation vector
            mut = a + self.F * (b - c)
            
            # Ensure mutation is within bounds
            min_b, max_b = self.bounds.T
            mut = np.clip(mut, min_b, max_b)
            pop_mut[i] = mut
            
        return pop_mut
    
    def crossover(self, population, pop_mut):
        """Apply binomial crossover"""
        pop_trial = np.zeros_like(population)
        
        for i in range(self.pop_size):
            cross_points = np.random.rand(self.dim) < self.CR
            # Ensure at least one parameter is crossed
            if not np.any(cross_points):
                cross_points[np.random.randint(0, self.dim)] = True
            pop_trial[i] = np.where(cross_points, pop_mut[i], population[i])
            
        return pop_trial
    
    def selection(self, population, pop_trial):
        """Select better solutions between current and trial populations"""
        pop_fitness = np.array([self.obj_func(ind) for ind in population])
        trial_fitness = np.array([self.obj_func(ind) for ind in pop_trial])
        
        idx = trial_fitness < pop_fitness
        population[idx] = pop_trial[idx]
        pop_fitness[idx] = trial_fitness[idx]
        
        return population, pop_fitness
    
    def optimize(self):
        """Run the differential evolution optimization"""
        # Initialize population
        population = self.init_population()
        best_fitness = float('inf')
        
        # Main optimization loop
        for iteration in range(self.max_iter):
            # Mutation
            pop_mut = self.mutation(population)
            
            # Crossover
            pop_trial = self.crossover(population, pop_mut)
            
            # Selection
            population, fitness = self.selection(population, pop_trial)
            
            # Update best solution
            curr_best = np.min(fitness)
            if curr_best < best_fitness:
                best_fitness = curr_best
                best_solution = population[np.argmin(fitness)]
                
            if iteration % 100 == 0:
                print(f'Iteration {iteration}: Best Fitness = {best_fitness}')
                
        return best_solution, best_fitness
