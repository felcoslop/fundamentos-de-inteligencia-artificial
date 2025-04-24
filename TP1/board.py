import numpy as np
from collections import deque
import copy

ROWS = 4
COLS = 4


class Board:
    """
    Cria o tabuleiro para o jogo.
    """

    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.board = np.zeros(shape=(self.rows, self.cols), dtype=int)

    def init_board(self):
        """
        Inicializa o tabuleiro com números de 0 a 15.
        """
        numbers = list(range(0, self.rows * self.cols))
        np.random.shuffle(numbers)
        self.board = np.array(numbers).reshape(self.rows, self.cols)

    def check_is_solvable(self):
        """
        Checa se a configuração atual do tabuleiro possui solução.
        """
        inversions = 0
        flat_board = self.board.flatten()

        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if (
                    flat_board[i] != 0
                    and flat_board[j] != 0
                    and flat_board[i] > flat_board[j]
                ):
                    inversions += 1

        blank_tile_row, _ = np.where(self.board == 0)

        blank_tile_row_from_bottom = self.rows - blank_tile_row[0]
        print("Index do número 0:", blank_tile_row_from_bottom)
        print("Paridade:", inversions)

        if blank_tile_row_from_bottom % 2 != 0:
            return inversions % 2 == 0

        else:
            return inversions % 2 != 0

    def get_neighbors(self, state):
        """
        Gera todos os estados vizinhos possíveis ao mover o 0.
        """
        neighbors = []
        rows, cols = self.rows, self.cols
        state = np.array(state).reshape((rows, cols))
        row, col = np.where(state == 0)
        row, col = row[0], col[0]

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                new_state = copy.deepcopy(state)
                new_state[row, col], new_state[r, c] = (
                    new_state[r, c],
                    new_state[row, col],
                )
                neighbors.append(new_state.flatten().tolist())

        return neighbors
    
    def manhattan_distance(self, state, goal_state):
        """
        Calcula a soma das distâncias de Manhattan para todas as peças.
        """
        state = np.array(state).reshape(self.rows, self.cols)
        goal_state = np.array(goal_state).reshape(self.rows, self.cols)
        distance = 0

        for i in range(self.rows):
            for j in range(self.cols):
                value = state[i, j]
                if value != 0:  # Ignora o espaço vazio
                    goal_i, goal_j = divmod(goal_state.flatten().tolist().index(value), self.cols)
                    distance += abs(i - goal_i) + abs(j - goal_j)

        return distance
    
    def misplaced_tiles(self, state, goal_state):
        """
        Conta o número de peças fora do lugar.
        """
        # Garante que state e goal_state sejam arrays do NumPy
        state = np.array(state).flatten()
        goal_state = np.array(goal_state).flatten()

        # Verifica se os tamanhos são iguais
        if state.size != goal_state.size:
            raise ValueError(f"Tamanhos incompatíveis: state ({state.size}) e goal_state ({goal_state.size})")

        # Conta as peças fora do lugar, ignorando o 0
        return np.sum((state != goal_state) & (goal_state != 0))
    
    def cost(self, path):
        """
        Calcula o custo acumulado (g(n)) com base no número de movimentos realizados.
        """
        return len(path)
