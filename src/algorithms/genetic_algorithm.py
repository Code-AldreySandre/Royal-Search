import random
from src.utils.board import calculate_collisions

POP_SIZE = 20
GENES_PER_QUEEN = 3 
CHROMOSOME_SIZE = 8 * GENES_PER_QUEEN
MUTATION_RATE = 0.03
CROSSOVER_RATE = 0.80
MAX_GENERATIONS = 1000

def decode_chromosome(bits):
    """Converte lista de 24 bits para lista de 8 inteiros (tabuleiro)."""
    board = []
    # Iterates every 3 bits
    for i in range(0, len(bits), GENES_PER_QUEEN):
        segment = bits[i:i+GENES_PER_QUEEN]
        # Convert binary to int
        val = int("".join(map(str, segment)), 2)
        board.append(val)
    return board

def fitness(bits):
    """
    Fitness for Roulette should be bigger = better.
    Max theoretical collisions = 28. Fitness = 28 - collisions.
    """
    board = decode_chromosome(bits)
    collisions = calculate_collisions(board)
    return 28 - collisions

def roulette_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choice(population)
    
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, score in zip(population, fitness_scores):
        current += score
        if current > pick:
            return individual
    return population[-1]

def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, CHROMOSOME_SIZE - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2
    return p1, p2

def mutate(individual):
    new_ind = individual[:]
    for i in range(len(new_ind)):
        if random.random() < MUTATION_RATE:
            new_ind[i] = 1 - new_ind[i] # Bit flip
    return new_ind

def genetic_algorithm():
    # Inicialization
    population = [[random.randint(0, 1) for _ in range(CHROMOSOME_SIZE)] for _ in range(POP_SIZE)]
    
    generation = 0
    best_solution = None
    best_collisions = float('inf')
    
    while generation < MAX_GENERATIONS:
        # Evaluation
        fitness_scores = [fitness(ind) for ind in population]
        
        max_fit = max(fitness_scores)
        elite_index = fitness_scores.index(max_fit)
        elite_individual = population[elite_index]
        
        current_collisions = 28 - max_fit
        if current_collisions < best_collisions:
            best_collisions = current_collisions
            best_solution = decode_chromosome(elite_individual)
        
        if current_collisions == 0: 
            break
            
        # Elitism
        new_pop = [elite_individual] 
        
        while len(new_pop) < POP_SIZE:
            parent1 = roulette_selection(population, fitness_scores)
            parent2 = roulette_selection(population, fitness_scores)
            
            child1, child2 = crossover(parent1, parent2)
            
            new_pop.append(mutate(child1))
            if len(new_pop) < POP_SIZE:
                new_pop.append(mutate(child2))
        
        population = new_pop
        generation += 1
        
    return best_solution, best_collisions, generation