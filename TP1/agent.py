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

    def solve_with_bfs(self):
        """
        Resolve o problema usando o algoritmo BFS.
        Retorna um relatório com:
        - Número de nós expandidos.
        - Número de movimentos até a solução.
        - Tempo até a solução.
        """
        if not self.board.check_is_solvable():
            return {
                "solution": None,
                "nodes_expanded": 0,
                "moves": 0,
                "time": 0,
            }

        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        queue = deque([(initial_state, [])])  # Fila para BFS: (estado, caminho)
        visited = set()
        nodes_expanded = 0  # Contador de nós expandidos

        start_time = time.time()  # Inicia o cronômetro

        while queue:
            current_state, path = queue.popleft()
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1  # Incrementa o contador de nós expandidos

            # Verifica se o estado atual é a solução
            if current_state == goal_state:
                end_time = time.time()  # Para o cronômetro
                return {
                    "solution": path + [current_state],
                    "nodes_expanded": nodes_expanded,
                    "moves": len(path),
                    "time": end_time - start_time,
                }

            # Gera os vizinhos e os adiciona à fila
            for neighbors in self.board.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    queue.append((neighbors, path + [current_state]))

        end_time = time.time()  # Para o cronômetro
        return {
            "solution": None,
            "nodes_expanded": nodes_expanded,
            "moves": 0,
            "time": end_time - start_time,
        }

    def solve_with_dfs(self):
        """
        Resolve o problema usando o algoritmo DFS.
        Retorna um relatório com:
        - Número de nós expandidos.
        - Número de movimentos até a solução.
        - Tempo até a solução.
        """
        if not self.board.check_is_solvable():
            return {
                "solution": None,
                "nodes_expanded": 0,
                "moves": 0,
                "time": 0,
            }

        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        stack = [(initial_state, [])]  # Pilha para DFS: (estado, caminho)
        visited = set()
        nodes_expanded = 0  # Contador de nós expandidos

        start_time = time.time()  # Inicia o cronômetro

        while stack:
            current_state, path = stack.pop()
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1  # Incrementa o contador de nós expandidos

            # Verifica se o estado atual é a solução
            if current_state == goal_state:
                end_time = time.time()  # Para o cronômetro
                return {
                    "solution": path + [current_state],
                    "nodes_expanded": nodes_expanded,
                    "moves": len(path),
                    "time": end_time - start_time,
                }

            # Gera os vizinhos e os adiciona à pilha
            for neighbors in self.board.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    stack.append((neighbors, path + [current_state]))

        end_time = time.time()  # Para o cronômetro
        return {
            "solution": None,
            "nodes_expanded": nodes_expanded,
            "moves": 0,
            "time": end_time - start_time,
        }

    def solve_with_a_star(self):
        """
        Resolve o problema usando o algoritmo A*.
        Retorna um relatório com:
        - Número de nós expandidos.
        - Número de movimentos até a solução.
        - Tempo até a solução.
        """
        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        # Fila de prioridade para armazenar os estados
        priority_queue = []
        visited = set()
        nodes_expanded = 0  # Contador de nós expandidos

        # Adiciona o estado inicial na fila de prioridade
        heappush(priority_queue, (0, 0, initial_state, []))  # (f(n), g(n), estado, caminho)

        start_time = time.time()  # Inicia o cronômetro

        while priority_queue:
            _, g, current_state, path = heappop(priority_queue)
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1  # Incrementa o contador de nós expandidos

            # Verifica se o estado atual é a solução
            if current_state == goal_state:
                end_time = time.time()  # Para o cronômetro
                return {
                    "solution": path + [current_state],
                    "nodes_expanded": nodes_expanded,
                    "moves": len(path),
                    "time": end_time - start_time,
                }

            # Gera os vizinhos e calcula f(n) para cada um
            for neighbors in self.board.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    h = self.board.misplaced_tiles(np.array(neighbors), np.array(goal_state))        # Calcula h(n)
                    g_new = self.board.cost(path + [current_state])                                  # Calcula g(n)
                    f = g_new + h                                                                    # Calcula f(n)
                    heappush(priority_queue, (f, g_new, neighbors, path + [current_state]))

        end_time = time.time()  # Para o cronômetro
        return {
            "solution": None,
            "nodes_expanded": nodes_expanded,
            "moves": 0,
            "time": end_time - start_time,
        }

    def solve_with_a_star(self, max_moves=50):
        """
        Resolve o problema usando o algoritmo A* com limite de movimentos.
        Retorna um relatório com:
        - Número de nós expandidos.
        - Número de movimentos até a solução.
        - Tempo até a solução.
        - Indicação se o limite de movimentos foi atingido.
        """
        initial_state = self.board.board.flatten().tolist()
        goal_state = list(range(1, self.board.rows * self.board.cols)) + [0]

        # Fila de prioridade para armazenar os estados
        priority_queue = []
        visited = set()
        nodes_expanded = 0  # Contador de nós expandidos

        # Adiciona o estado inicial na fila de prioridade
        heappush(priority_queue, (0, 0, initial_state, []))  # (f(n), g(n), estado, caminho)

        start_time = time.time()  # Inicia o cronômetro

        while priority_queue:
            _, g, current_state, path = heappop(priority_queue)
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            nodes_expanded += 1  # Incrementa o contador de nós expandidos

            # Verifica se o número de movimentos excede o limite
            if len(path) > max_moves:
                end_time = time.time()  # Para o cronômetro
                return {
                    "solution": None,
                    "nodes_expanded": nodes_expanded,
                    "moves": len(path),
                    "time": end_time - start_time,
                    "limit_reached": True,  # Indica que o limite foi atingido
                }

            # Verifica se o estado atual é a solução
            if current_state == goal_state:
                end_time = time.time()  # Para o cronômetro
                return {
                    "solution": path + [current_state],
                    "nodes_expanded": nodes_expanded,
                    "moves": len(path),
                    "time": end_time - start_time,
                    "limit_reached": False,  # Indica que o limite não foi atingido
                }

            # Gera os vizinhos e calcula f(n) para cada um
            for neighbors in self.board.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    h = self.board.misplaced_tiles(np.array(neighbors), np.array(goal_state))  # Calcula h(n)
                    g_new = self.board.cost(path + [current_state])  # Calcula g(n)
                    f = g_new + h  # Calcula f(n)
                    heappush(priority_queue, (f, g_new, neighbors, path + [current_state]))

        end_time = time.time()  # Para o cronômetro
        return {
            "solution": None,
            "nodes_expanded": nodes_expanded,
            "moves": 0,
            "time": end_time - start_time,
            "limit_reached": False,  # Indica que o limite não foi atingido
        }

    def misplaced_tiles(self, state, goal_state):
        """
        Conta o número de peças fora do lugar.
        """
        # Garante que state e goal_state sejam arrays do NumPy
        state = np.array(state).flatten()
        goal_state = np.array(goal_state).flatten()

        # Conta as peças fora do lugar, ignorando o 0
        return np.sum((state != goal_state) & (goal_state != 0))