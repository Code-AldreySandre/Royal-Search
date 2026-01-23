import random

def calculate_colissions(board):
    """
    Calculates the number of pairs of queens attacking each other.
    Board is a list of 8 integers, where the index is the column and the value is the row.
    """
    n = len(board)
    collisions = 0
    for i in range(n):

        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                collisions += 1
                
    return collisions

def random_board():
    """Gera um tabuleiro aleatório (vetor de 0 a 7)."""
    return [random.randint(0, 7) for _ in range(8)]
