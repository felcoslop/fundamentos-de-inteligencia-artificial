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

    def init_board(self, initial_state=None):
        """
        Inicializa o tabuleiro.
        - Se `initial_state` for fornecido, usa-o como estado inicial.
        - Caso contrário, gera um tabuleiro aleatório.
        """
        if initial_state:
            # Usa o estado inicial fornecido
            self.board = np.array(initial_state).reshape(self.rows, self.cols)
            self.check_is_solvable()
            if not self.check_is_solvable():
                raise ValueError("O tabuleiro inicial não é solucionável.")
        else:
            # Gera um tabuleiro aleatório
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

    def misplaced_tiles(self, state, goal_state):
        """
        Conta o número de peças fora do lugar.
        """
        return np.sum(state != goal_state) - 1  # Ignora o 0
    
    def cost(self, path):
        """
        Calcula o custo acumulado (g(n)) com base no número de movimentos realizados.
        """
        return len(path)
