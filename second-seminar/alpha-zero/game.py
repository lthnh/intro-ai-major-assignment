import numpy as np
import numpy.typing as npt

class UltimateTicTacToe():
    __sub_board_indices = ((0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6))
    def get_initial_board(self):
        # 0: canonical form
        # 1: turn (1 for X and 0 for O)
        # 2: won sub boards
        return np.zeros((3, 9, 9))
    def get_next_state(self, board: npt.NDArray, action: tuple):
        board[action[0]][action[1]] = board[1][0]
        return board
    def get_valid_moves(self, board: npt.NDArray) -> list[tuple[int, int]]:
        return list(zip(*np.where(board == 0)))
    def get_game_ended(self, board: npt.NDArray):
        pass
    def _check_sub_board(self, board):
        for r, c in self.__sub_board_indices:
            sub_board = board[r:r+3][c:c+3]
            column_sum = sub_board.sum(axis=0)
            row_sum = sub_board.sum(axis=1)
            neg_diag_sum = sub_board.trace()
            pos_diag_sum = np.rot90(sub_board).trace()
            