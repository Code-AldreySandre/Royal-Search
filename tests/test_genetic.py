from src.algorithms.genetic_algorithm import decode_chromosome, fitness

def test_decode_chromosome():
    """
    Testa se a conversão de 24 bits para 8 inteiros funciona.
    Exemplo: 000 -> 0, 111 -> 7
    """
    # 3 bits * 8 rainhas
    # Vamos criar um cromossomo que resulta em [0, 7, 0, 7, ...]
    # 000 (0), 111 (7)
    gene_zero = [0, 0, 0]
    gene_seven = [1, 1, 1]
    
    chromosome = []
    expected_board = []
    
    # Monta 4 pares de (0, 7)
    for _ in range(4):
        chromosome.extend(gene_zero)
        expected_board.append(0)
        chromosome.extend(gene_seven)
        expected_board.append(7)
        
    decoded_board = decode_chromosome(chromosome)
    
    assert len(decoded_board) == 8
    assert decoded_board == expected_board

def test_fitness_function_inversion():
    """
    Testa se o fitness do GA está invertendo corretamente (28 - colisões).
    """
    # Cromossomo representando a solução ótima do PDF (0 colisões)
    # [4, 2, 0, 6, 1, 7, 5, 3]
    # 4=100, 2=010, 0=000, 6=110, 1=001, 7=111, 5=101, 3=011
    
    # Montando manualmente os bits da solução
    optimal_bits = [
        1,0,0, # 4
        0,1,0, # 2
        0,0,0, # 0
        1,1,0, # 6
        0,0,1, # 1
        1,1,1, # 7
        1,0,1, # 5
        0,1,1  # 3
    ]
    
    # Se colisões = 0, fitness deve ser 28
    score = fitness(optimal_bits)
    assert score == 28