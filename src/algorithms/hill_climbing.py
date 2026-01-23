import random
from src.utils.board import calculate_collisions, random_board

def get_random_neighbor(board):
    """Gera um vizinho movendo uma rainha aleatória para uma nova linha aleatória."""
    neighbor = board[:]
    col = random.randint(0, 7)
    current_row = neighbor[col]
    

    new_row = random.randint(0, 7)
    while new_row == current_row:
        new_row = random.randint(0, 7)
        
    neighbor[col] = new_row
    return neighbor

def stochastic_hill_climbing(max_no_improve=500):
    current_state = random_board()
    current_fitness = calculate_collisions(current_state)
    
    no_improve_count = 0
    iterations = 0
    
    while no_improve_count < max_no_improve:
        if current_fitness == 0: 
            break
            
        iterations += 1
        neighbor = get_random_neighbor(current_state)
        neighbor_fitness = calculate_collisions(neighbor)
        
    
        if neighbor_fitness < current_fitness:
            current_state = neighbor
            current_fitness = neighbor_fitness
            no_improve_count = 0 
        else:
            no_improve_count += 1
            
    return current_state, current_fitness, iterations