import pickle
from copy import copy

import numpy as np
import numpy.typing as npt

from ..state import State, UltimateTTT_Move
from .uttt_nnet import UTTTNeuralNetwork
from .transform import encode

epsilon = 1e-6 # prevent the U term from being 0 when unexplored (N = 0)


class MonteCarlosTreeSearch():
    def __init__(self, nn: UTTTNeuralNetwork):
        self.nn = nn
        self.tree = dict()
    
    def get_action_distribution(self, )

    def search(self, state: State, cpuct: float = 1.0):
        s = pickle.dumps(state)
