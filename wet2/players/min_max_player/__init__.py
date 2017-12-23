import abstract
from utils import *
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import time
import copy
import math
import numpy as np
import heuristics

class Player(abstract.AbstractPlayer):


    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time,
                                         player_color, time_per_k_turns, k)
        self.clock = time.time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = \
            self.time_remaining_in_round / self.turns_remaining_in_round - 0.05



    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        alg = MiniMaxAlgorithm(self.heuristic, self.color, self.no_more_time, None)

        bestMove = None
        bestVal = None
        d = 1
        try:
            while True:
                bestVal, bestMove = alg.search(game_state, d, True)
                d+=1
        except ExceededTimeError:
            pass


        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

        return bestMove


    def heuristic(self, state):
        return heuristics.smart_heuristic(state, self.color)

    def no_more_time(self):

        return (time.time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'min_max')
