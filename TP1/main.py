from board import Board
from agent import Agent
from tabulate import tabulate  # Biblioteca para formatar a saída como tabela
import numpy as np

def initialize_board(use_random):
    """
    Inicializa o tabuleiro.
    - Se `use_random` for True, gera um tabuleiro aleatório.
    - Caso contrário, usa um tabuleiro fixo para testes.
    """
    board = Board()
    if use_random:
        board.init_board()  # Gera um tabuleiro aleatório
    else:
        # Define um tabuleiro fixo para testes
        initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12]
        board.init_board(initial_state=initial_state)
    # Verifica se o tabuleiro é solucionável
    if not board.check_is_solvable():
        print("Tabuleiro não solucionável. Gerando um novo tabuleiro.")
        board.init_board()  # Gera um novo tabuleiro se o atual não for solucionável
    else:
        print("Tabuleiro inicial gerado com sucesso.")
    return board


def display_results(results):
    """
    Exibe os resultados em formato de tabela.
    """
    headers = ["Método", "Nós Expandidos", "Movimentos", "Tempo"]
    print("\nRelatório Final:")
    print(tabulate(results, headers=headers, tablefmt="grid"))


def solve_and_collect_results(agent, max_moves=50):
    """
    Resolve o problema usando diferentes algoritmos e coleta os resultados.
    """
    results = []

    # Resolver com A*
    print("\nSolução usando A*:")
    a_star_report = agent.solve_with_a_star(max_moves=max_moves)
    if a_star_report["solution"]:
        print("Caminho da solução encontrado com A*:")
        for step in a_star_report["solution"]:
            print(step)
        results.append([
            "A*", a_star_report["nodes_expanded"], a_star_report["moves"], f"{a_star_report['time']:.4f} segundos"
        ])
    else:
        if a_star_report["limit_reached"]:
            print("O limite de movimentos foi atingido antes de encontrar a solução.")
        else:
            print("Nenhuma solução encontrada.")
        results.append(["A*", "N/A", "N/A", "N/A"])

    # Resolver com BFS
    print("\nSolução usando BFS:")
    bfs_report = agent.solve_with_bfs()
    if bfs_report["solution"]:
        print("Caminho da solução encontrado com BFS:")
        for step in bfs_report["solution"]:
            print(step)
        results.append([
            "BFS", bfs_report["nodes_expanded"], bfs_report["moves"], f"{bfs_report['time']:.4f} segundos"
        ])
    else:
        print("Nenhuma solução encontrada com BFS.")
        results.append(["BFS", "N/A", "N/A", "N/A"])

    # Resolver com DFS
    print("\nSolução usando DFS:")
    dfs_report = agent.solve_with_dfs()
    if dfs_report["solution"]:
        print("Caminho da solução encontrado com DFS:")
        for step in dfs_report["solution"]:
            print(step)
        results.append([
            "DFS", dfs_report["nodes_expanded"], dfs_report["moves"], f"{dfs_report['time']:.4f} segundos"
        ])
    else:
        print("Nenhuma solução encontrada com DFS.")
        results.append(["DFS", "N/A", "N/A", "N/A"])

    return results


def compare_methods(num_trials=5, max_moves=100):
    """
    Executa os métodos de busca em várias configurações iniciais e calcula métricas médias.
    """
    # Estruturas para armazenar métricas
    metrics = {
        "A*": {"nodes_expanded": [], "moves": [], "time": []},
        "BFS": {"nodes_expanded": [], "moves": [], "time": []},
        "DFS": {"nodes_expanded": [], "moves": [], "time": []}
    }

    for trial in range(num_trials):
        print(f"\n=== Teste {trial + 1}/{num_trials} ===")
        # Inicializa um tabuleiro aleatório solucionável
        board = initialize_board(use_random=True)
        print("Tabuleiro inicial:")
        print(board.board)

        # Inicializa o agente
        agent = Agent(board)

        # Executa os métodos de busca
        results = solve_and_collect_results(agent, max_moves=max_moves)

        # Coleta métricas de cada método
        for method, nodes, moves, time in results:
            if nodes != "N/A":
                metrics[method]["nodes_expanded"].append(int(nodes))
                metrics[method]["moves"].append(int(moves))
                metrics[method]["time"].append(float(time.split()[0]))  # Extrai o valor numérico do tempo
            else:
                metrics[method]["nodes_expanded"].append(0)
                metrics[method]["moves"].append(0)
                metrics[method]["time"].append(0)

    # Calcula médias
    summary = []
    for method in metrics:
        nodes_avg = np.mean(metrics[method]["nodes_expanded"]) if metrics[method]["nodes_expanded"] else "N/A"
        moves_avg = np.mean(metrics[method]["moves"]) if metrics[method]["moves"] else "N/A"
        time_avg = np.mean(metrics[method]["time"]) if metrics[method]["time"] else "N/A"
        summary.append([
            method,
            f"{nodes_avg:.2f}" if isinstance(nodes_avg, float) else nodes_avg,
            f"{moves_avg:.2f}" if isinstance(moves_avg, float) else moves_avg,
            f"{time_avg:.4f} segundos" if isinstance(time_avg, float) else time_avg
        ])

    # Exibe resultados médios
    print(f"\n=== Resumo após {num_trials} testes ===")
    display_results(summary)

if __name__ == "__main__":
    import argparse

    # Configuração de argumentos
    parser = argparse.ArgumentParser(description="15-Puzzle Solver")
    parser.add_argument("--random", action="store_true", help="Usar tabuleiro aleatório")
    parser.add_argument("--compare", action="store_true", help="Executar comparação de métodos")
    parser.add_argument("--trials", type=int, default=5, help="Número de testes para comparação")
    args = parser.parse_args()

    if args.compare:
            # Executa a comparação com múltiplos testes
            compare_methods(num_trials=args.trials, max_moves=100)
    else:
        # Executa o fluxo original para um único tabuleiro
        board = initialize_board(use_random=args.random)
        print("Tabuleiro inicial:")
        print(board.board)
        agent = Agent(board)
        results = solve_and_collect_results(agent, max_moves=100)
        display_results(results)