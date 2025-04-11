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

    def bfs(self, initial_state):
        """
        Breadth-First-Search to solve the 15 puzzle.

        1. Começa no estado inicial (puzzle em uma configuração aleatória)
        2. Coloca o estado inicial na fila
        3. Retira o estado da fila
        4. Veja se é solução
        5. Se não for solução, gere os vizinhos possíveis (movimentos do 0)
        6. Adicione os vizinhos na fila
        7. Veja se é solução (se não for, repete desde o passo 3)
        """
        initial_state = initial_state.flatten().tolist()
        goal_state = list(range(1, self.rows * self.cols)) + [0]
        queue = deque()
        visited = set()

        queue.append((initial_state, []))

        while queue:
            current_state, path = queue.popleft()
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            if current_state == goal_state:
                return path + [current_state]

            for neighbors in self.get_neighbors(current_state):
                if tuple(neighbors) not in visited:
                    queue.append((neighbors, path + [current_state]))
        return None


board1 = Board()
board1.init_board()
print(board1.board)
if board1.check_is_solvable():
    print(board1.bfs(board1.board))

# print(board1.get_neighbors(board1.board))
