import pickle
from collections import deque
import numpy as np
import numpy.typing as npt

from .state import State, UltimateTTT_Move
from .uttt_nnet import UTTTNeuralNetwork
from .transform import encode
from .utils import SubBoardIndex

class MonteCarloTreeSearch():
    def __init__(self, state: State, nnet: UTTTNeuralNetwork, args):
        self.state = state
        self.nnet = nnet
        self.args = args
        self.Qsa = {}
        self.Nsa = {}
        self.Ns = {}
        self.Ps = {}

        self.Es = {}
        self.Vs = {}

    def getActionProb(self, temp=1):
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.

        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)
        """
        for i in range(self.args.num_sims):
            self.search()
        s = pickle.dumps(self.state)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]
        if temp == 0:
            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)
            probs[bestA] = 1
            return probs
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in counts]
        return probs

    def search(self):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propagated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propagated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.

        Returns:
            v: the negative of the value of the current canonicalBoard
        """
        stack = deque()
        origin_state = pickle.dumps(self.state)
        stack.append(origin_state)
        while len(stack)>0:
            s = stack.pop()
            state: State = pickle.loads(s)
            if s not in self.Es:
                self.Es[s] = state.game_result(state.global_cells)
            if self.Es[s] not in [None, 0]:
                # terminal node
                return -self.Es[s]
            if s not in self.Ps:
                # leaf node
                self.Ps[s], v = self.nnet.predict(encode(state))
                valids_move: list[UltimateTTT_Move] = state.get_valid_moves
                valids_mask: npt.ArrayLike = np.zeros(shape=(9, 9))
                for move in valids_move:
                    local_idx = move.index_local_board
                    row_idx = SubBoardIndex[local_idx][0] + move.x
                    col_idx = SubBoardIndex[local_idx][1] + move.y
                    valids_mask[row_idx, col_idx] = 1
                valids_mask.flatten()
            
