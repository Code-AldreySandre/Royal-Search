import random

def calculate_collisions(board):
    n = len(board)
    collisions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                collisions += 1
    return collisions

def random_board():
    return [random.randint(0, 7) for _ in range(8)]