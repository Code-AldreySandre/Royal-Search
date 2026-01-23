import os
import time
import pandas as pd
from tqdm import tqdm

from src import logger, DATA_DIR 
from src.algorithms.hill_climbing import stochastic_hill_climbing
from src.algorithms.genetic_algorithm import genetic_algorithm

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def run_experiment(algorithm_func, algorithm_name, n_runs=50):
    results = []
    
    logger.info(f"Iniciando 50 execuções para: {algorithm_name}...")
    
    for i in tqdm(range(n_runs), desc=algorithm_name, ncols=100):
        start_time = time.time()
        
        solution, collisions, iterations = algorithm_func()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        results.append({
            "Algoritmo": algorithm_name,
            "Execução": i + 1,
            "Solução": str(solution),
            "Colisões": collisions,
            "Iterações": iterations,
            "Tempo (s)": execution_time
        })
    
    logger.info(f"Finalizado: {algorithm_name}")
    return pd.DataFrame(results)

def generate_report(df, algorithm_name):
    print(f"\n{'='*20} RELATÓRIO: {algorithm_name} {'='*20}")
    
    stats = df[["Iterações", "Tempo (s)"]].describe().loc[['mean', 'std']]
    print("\nEstatísticas (Média e Desvio Padrão):")
    print(stats)
    
    mean_time = stats.loc['mean', 'Tempo (s)']
    mean_iter = stats.loc['mean', 'Iterações']
    logger.info(f"Stats {algorithm_name}: Média Tempo={mean_time:.4f}s, Média Iter={mean_iter:.1f}")

    df_sorted = df.sort_values(by="Colisões", ascending=True)
    unique_solutions = df_sorted.drop_duplicates(subset=["Solução"])
    
    print("\n As 5 melhores soluções distintas:")
    top_5 = unique_solutions.head(5)
    for index, row in top_5.iterrows():
        print(f"   Rank {index}: Colisões={row['Colisões']} | Iterações={row['Iterações']} | Board={row['Solução']}")

def main():
    try:
        # Hill Climbing
        df_hc = run_experiment(stochastic_hill_climbing, "Stochastic Hill Climbing")
        generate_report(df_hc, "Stochastic Hill Climbing")
        
        # Genetic Algorithm
        df_ga = run_experiment(genetic_algorithm, "Genetic Algorithm")
        generate_report(df_ga, "Genetic Algorithm")
        
        # Saving CSVs
        hc_path = os.path.join(DATA_DIR, "logs_hill_climbing.csv")
        ga_path = os.path.join(DATA_DIR, "logs_genetic.csv")
        
        df_hc.to_csv(hc_path, index=False)
        df_ga.to_csv(ga_path, index=False)
        
        logger.info(f"Bases de dados salvas em: {DATA_DIR}")
        
    except Exception as e:
        logger.error(f"Erro fatal na execução: {e}", exc_info=True)

if __name__ == "__main__":
    main()