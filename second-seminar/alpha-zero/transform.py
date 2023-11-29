from itertools import product
import numpy as np
import numpy.typing as npt
import torch

from ..state import State, UltimateTTT_Move
from .utils import SubBoardIndex

def encode(state: State):
    # start_idx = tuple(product((0, 3, 6), (0, 3, 6)))
    start_idx = SubBoardIndex
    encoded_state = np.zeros(shape=(4, 9, 9))
    # 0: current player
    # 1: for opponent
    assert state.player_to_move in {state.X, state.O}
    if state.player_to_move == state.X:
        x_idx = 0
        o_idx = 1
    else:
        x_idx = 1
        o_idx = 0
    t: int = 0
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block: npt.ArrayLike = state.blocks[t]
            block_x = np.clip(block, 0, 1)
            block_o = np.clip(np.negative(block), 0, 1)
            encoded_state[x_idx][i:i+3, j:j+3] = block_x
            encoded_state[o_idx][i:i+3, j:j+3] = block_o
            t += 1
    # 2: fill 1 or 0 depending on the current player (X or 0)
    if state.player_to_move == state.X:
        encoded_state[2].fill(1)
    else:
        encoded_state[2].fill(0)
    # 3: current player's legal moves
    legal_moves: list[UltimateTTT_Move] = state.get_valid_moves
    for move in legal_moves:
        local_board_idx = move.index_local_board
        row_idx = start_idx[local_board_idx][0] + move.x
        col_idx = start_idx[local_board_idx][1] + move.y
        encoded_state[3][row_idx][col_idx] = 1
    return encoded_state

def decode(global_state: torch.Tensor, block_state: torch.Tensor):
    pass