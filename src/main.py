import os
import time
import pandas as pd
from tqdm import tqdm
from src import logger, DATA_DIR 
from src.algorithms.hill_climbing import stochastic_hill_climbing
from src.algorithms.genetic_algorithm import genetic_algorithm

pd.set_option('display.max_columns', None)

def run_experiment(algorithm_func, algorithm_name, n_runs=50, max_len=1000):
    results = []
    convergence_data = []
    
    logger.info(f"Iniciando {n_runs} execuções para: {algorithm_name}...")
    
    for i in tqdm(range(n_runs), desc=algorithm_name, ncols=100):
        start_time = time.time()
        
        solution, collisions, iterations, history = algorithm_func()
        
        end_time = time.time()
        
        if len(history) < max_len:
            last_val = history[-1]
            padding = [last_val] * (max_len - len(history))
            history.extend(padding)
        else:
            history = history[:max_len]
            
        convergence_data.append(history)
        
        results.append({
            "Algoritmo": algorithm_name,
            "Execução": i + 1,
            "Solução": str(solution),
            "Colisões": collisions,
            "Iterações": iterations,
            "Tempo (s)": end_time - start_time
        })
    
    logger.info(f"Finalizado: {algorithm_name}")
    
    df_summary = pd.DataFrame(results)
    df_convergence = pd.DataFrame(convergence_data)
    
    return df_summary, df_convergence

def main():
    try:
        df_hc, conv_hc = run_experiment(stochastic_hill_climbing, "Stochastic Hill Climbing", max_len=1000)
        df_ga, conv_ga = run_experiment(genetic_algorithm, "Genetic Algorithm", max_len=1000)
        
        df_hc.to_csv(os.path.join(DATA_DIR, "logs_hill_climbing.csv"), index=False)
        df_ga.to_csv(os.path.join(DATA_DIR, "logs_genetic.csv"), index=False)
        
        conv_hc.to_csv(os.path.join(DATA_DIR, "convergence_hc.csv"), index=False)
        conv_ga.to_csv(os.path.join(DATA_DIR, "convergence_ga.csv"), index=False)
        
        logger.info(f"Dados salvos em: {DATA_DIR}")
        
    except Exception as e:
        logger.error(f"Erro: {e}", exc_info=True)

if __name__ == "__main__":
    main()