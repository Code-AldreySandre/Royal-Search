import pytest
from src.utils.board import calculate_collisions

def test_pdf_solution_has_zero_collisions():
    """
    Testa a solução exata fornecida na imagem do PDF.
    Array: [4, 2, 0, 6, 1, 7, 5, 3]
    """
    # Questão 1
    solution_board = [4, 2, 0, 6, 1, 7, 5, 3]
    assert calculate_collisions(solution_board) == 0

def test_diagonal_collision():
    """
    Testa duas rainhas se atacando na diagonal.
    (0,0) e (1,1) se atacam.
    """
    # Tabuleiro onde as duas primeiras rainhas estão na diagonal
    # O resto está longe pra não interferir
    board = [0, 1, 3, 4, 5, 6, 7, 2]
    # Pelo menos 1 colisão deve ser detectada
    assert calculate_collisions(board) >= 1

def test_linear_collision():
    """
    Testa duas rainhas na mesma linha.
    """
    # Rainha da col 0 na linha 0
    # Rainha da col 1 na linha 0
    board = [0, 0, 2, 3, 4, 5, 6, 7] 
    assert calculate_collisions(board) >= 1