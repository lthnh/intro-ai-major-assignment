from typing import Union, Optional
from copy import copy
import pickle

import numpy as np
import numpy.typing as npt

from ..state import State, UltimateTTT_Move
from .uttt_nnet import UTTTNeuralNetwork
from .transform import encode
from .utils import SubBoardIndex

epsilon = 1e-6 # prevent the U term from being 0 when unexplored (N = 0)


class MonteCarlosTreeSearch():
    def __init__(self, nn: UTTTNeuralNetwork):
        self.nn = nn
        self.tree = dict()

    def search(self, state: State, cpuct: float = 1.0):
        s: bytes = pickle.dumps(state)
        curr_player = state.player_to_move
        if s in self.tree:
            pass
        else:
            e: Union[int, None] = state.game_result
            if e != None:
                return -e
            available_actions: list[Optional[UltimateTTT_Move]] = state.get_valid_moves
            pi, v = self.nn.predict(encode(state))
            pi.reshape((9, 9))
            actions_mask = np.zeros((9, 9))
            for action in available_actions:
                local_board_idx = action.index_local_board
                row_idx = local_board_idx[0] + action.x
                column_idx = local_board_idx[1] + action.y
                actions_mask[row_idx][column_idx] = 1
            pi = np.multiply(pi, actions_mask)
            total_prob = pi.sum()
            if total_prob > 0:
                pi /= total_prob
            else:
                print("All valid moves were masked, doing a workaround")
                pi = pi + actions_mask
                pi /= total_prob
            stats = []
            stats[:, 3] = pi[pi != 0]
            stats[:, 0] = 




    def get_action_distribution(self, state: State, temperature=1):
        pass
