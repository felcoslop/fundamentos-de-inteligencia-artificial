import time
import numpy as np
from heapq import heappush, heappop
from collections import deque


class Agent:
    """
    Agente que resolve o problema do 15-puzzle usando BFS, DFS ou A*.
    """

    def __init__(self, board):
        """
        Inicializa o agente com um tabuleiro.
        """
        self.board = board

    def _generate_report(self, solution, nodes_expanded, moves, start_time, limit_reached=False):
        """
        Gera um relatório com os resultados da busca.
        """
        end_time = time.time()
        return {
            "solution": solution,
            "nodes_expanded": nodes_expanded,
            "moves": moves,
            "time": end_time - start_time,
            "limit_reached": limit_reached,
        }

    def solve_with_a_star(self, max_moves=50):
        """
        Resolve o problema usando o algoritmo A* com limite de movimentos.
        """
        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        priority_queue = []
        visited = set()
        nodes_expanded = 0

        heappush(priority_queue, (0, 0, initial_state, []))  # (f(n), g(n), estado, caminho)
        start_time = time.time()

        while priority_queue:
            _, g, current_state, path = heappop(priority_queue)
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1

            if nodes_expanded > 10000:  # Limite de nós expandidos
                print("Limite de nós expandidos atingido. Interrompendo a busca.")
                return self._generate_report(None, nodes_expanded, len(path), start_time, limit_reached=True)

            if len(path) > max_moves:
                return self._generate_report(None, nodes_expanded, len(path), start_time, limit_reached=True)

            if np.array_equal(current_state, goal_state):
                return self._generate_report(path + [current_state], nodes_expanded, len(path), start_time)

            for neighbors in self.board.get_neighbors(current_state):
                try:
                    # Garante que neighbors e goal_state sejam arrays NumPy com o mesmo tamanho
                    neighbors = np.array(neighbors).flatten()
                    goal_state = np.array(goal_state).flatten()

                    if neighbors.size != goal_state.size:
                        raise ValueError("O estado vizinho não tem o mesmo tamanho que o estado objetivo.")

                    # Calcula h(n) e g(n)
                    h = self.board.manhattan_distance(neighbors, goal_state)
                    g_new = self.board.cost(path + [current_state])
                    f = g_new + h

                    # Adiciona o estado vizinho à fila de prioridade
                    heappush(priority_queue, (f, g_new, neighbors.tolist(), path + [current_state]))
                except Exception as e:
                    # Ignora estados vizinhos inválidos e continua
                    print(f"Estado vizinho inválido ignorado: {e}")

        return self._generate_report(None, nodes_expanded, 0, start_time)

    def solve_with_bfs(self):
        """
        Resolve o problema usando o algoritmo BFS.
        """
        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        queue = deque([(initial_state, [])])
        visited = set()
        nodes_expanded = 0
        start_time = time.time()

        while queue:
            current_state, path = queue.popleft()
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1

            if nodes_expanded > 10000:  # Limite de nós expandidos
                print("Limite de nós expandidos atingido. Interrompendo a busca.")
                return self._generate_report(None, nodes_expanded, len(path), start_time, limit_reached=True)

            if current_state == goal_state:
                return self._generate_report(path + [current_state], nodes_expanded, len(path), start_time)

            for neighbors in self.board.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    queue.append((neighbors, path + [current_state]))

        return self._generate_report(None, nodes_expanded, 0, start_time)

    def solve_with_dfs(self):
        """
        Resolve o problema usando o algoritmo DFS.
        """
        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        stack = [(initial_state, [])]
        visited = set()
        nodes_expanded = 0
        start_time = time.time()

        while stack:
            current_state, path = stack.pop()
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1

            if nodes_expanded > 10000:  # Limite de nós expandidos
                print("Limite de nós expandidos atingido. Interrompendo a busca.")
                return self._generate_report(None, nodes_expanded, len(path), start_time, limit_reached=True)

            if current_state == goal_state:
                return self._generate_report(path + [current_state], nodes_expanded, len(path), start_time)

            for neighbors in self.board.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    stack.append((neighbors, path + [current_state]))

        return self._generate_report(None, nodes_expanded, 0, start_time)