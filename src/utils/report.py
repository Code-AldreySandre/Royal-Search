import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from src.algorithms.hill_climbing import stochastic_hill_climbing
from src.algorithms.genetic_algorithm import genetic_algorithm
from src.utils.board import calculate_collisions


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def run_experiment(algorithm_func, algorithm_name, n_runs=50):
    results = []
    
    print(f"\nIniciando 50 execuções para: {algorithm_name}...")
    
    for i in tqdm(range(n_runs)):
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
    
    return pd.DataFrame(results)

def generate_report(df, algorithm_name):
    print(f"\n{'='*20} RELATÓRIO: {algorithm_name} {'='*20}")
    
    stats = df[["Iterações", "Tempo (s)"]].describe().loc[['mean', 'std']]
    print("\nEstatísticas (Média e Desvio Padrão):")
    print(stats)
    
    df_sorted = df.sort_values(by="Colisões", ascending=True)
    
    unique_solutions = df_sorted.drop_duplicates(subset=["Solução"])
    
    print("\n🏆 Top 5 Soluções Distintas:")
    top_5 = unique_solutions.head(5)
    
    for index, row in top_5.iterrows():
        print(f"   Rank {index}: Colisões={row['Colisões']} | Iterações={row['Iterações']} | Board={row['Solução']}")

def main():
    df_hc = run_experiment(stochastic_hill_climbing, "Stochastic Hill Climbing")
    generate_report(df_hc, "Stochastic Hill Climbing")
    
    df_ga = run_experiment(genetic_algorithm, "Genetic Algorithm")
    generate_report(df_ga, "Genetic Algorithm")
    
    df_hc.to_csv("logs_hill_climbing.csv", index=False)
    df_ga.to_csv("logs_genetic.csv", index=False)
    print("\nLogs salvos em CSV com sucesso!")

if __name__ == "__main__":
    main()