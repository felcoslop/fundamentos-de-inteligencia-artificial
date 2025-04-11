import numpy as np

ROWS = 4
COLS = 4


class Board:
    """
    Creates the board for the game.
    """

    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.board = np.zeros(shape=(self.rows, self.cols), dtype=int)

    def init_board(self):
        """
        Initialize the board with numbers from 0 to 15.
        """
        numbers = list(range(0, self.rows * self.cols))
        np.random.shuffle(numbers)
        self.board = np.array(numbers).reshape(self.rows, self.cols)

    def check_is_solvable(self):
        """
        Check if the board is solvable.
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


board1 = Board()
board1.init_board()
print(board1.board)
print(board1.check_is_solvable())
