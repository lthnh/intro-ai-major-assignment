from typing import Optional

import numpy as np
import numpy.typing as npt

class UltimateTicTacToe():
    __sub_board_indices = ((0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6))
    def get_initial_board(self):
        # 0: canonical form
        # 1: turn (1 for X and 0 for O)
        # 2: last move
        # 3: won sub boards
        return np.zeros((4, 9, 9))
    def get_next_state(self, board: npt.NDArray, action: tuple):
        board[0][action[0]][action[1]] = 1 if board[1][0] else -1
        return board
    def get_valid_moves(self, board: npt.NDArray) -> list[Optional[tuple[int, int]]]:
        last_move: tuple[int, int] = (idx.item() for idx in board[2].nonzero())
        empty_position_global: list[tuple[int, int]] = list(zip(*np.where(board == 0)))
        legal_moves = []
        for r, c in self.__sub_board_indices:
            if last_move[0] >= r and last_move[1] >= c:
                relative_row = last_move[0] - r
                relative_column = last_move[1] - c
                relative_idx = 3*relative_row + relative_column
                sub_board_next_row, sub_board_next_column = self.__sub_board_indices[relative_idx]
                sub_board_next = board[sub_board_next_row:sub_board_next_row+3][sub_board_next_column:sub_board_next_column+3]
                empty_position_local = np.argwhere(sub_board_next == 0)
                legal_moves = empty_position_local if len(empty_position_local) > 0 else empty_position_global
                return legal_moves
    def get_game_ended(self, board: npt.NDArray):
        
        pass
    def _check_result_sub_boards(self, board):
        for r, c in self.__sub_board_indices:
            sub_board = board[r:r+3][c:c+3]
            column_sum = sub_board.sum(axis=0)
            row_sum = sub_board.sum(axis=1)
            negative_diagonal_sum = sub_board.trace()
            positive_diagonal_sum = np.rot90(sub_board).trace()