import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import time
import copy
import math
import heuristics
import numpy as np

#Consts:
LAST_COL = BOARD_COLS - 1
LAST_ROW = BOARD_ROWS - 1
CORNER_INDICES = [(LAST_COL, 0), (0, 0), (LAST_COL, LAST_ROW), (0, LAST_ROW)]






class Player(abstract.AbstractPlayer):


    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time,
                                         player_color, time_per_k_turns, k)
        self.clock = time.time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        self.openingsDict = heuristics.getPartialOpeningsDict()

    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        #Try to get move from openings book:
        opening = self.opening_move(game_state)


        if opening:
            return opening



        best_move = possible_moves[0]
        next_state = copy.deepcopy(game_state)
        next_state.perform_move(best_move[0],best_move[1])
        # Choosing an arbitrary move
        # Get the best move according the utility function
        for move in possible_moves:
            new_state = copy.deepcopy(game_state)
            new_state.perform_move(move[0],move[1])
            if self.heuristic(new_state) > self.heuristic(next_state):
                next_state = new_state
                best_move = move

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

        return best_move

    def heuristic(self, state):
        return heuristics.smart_heuristic(state, self.color)

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better')


    def opening_move(self, state):
        if state in self.openingsDict:
            return self.openingsDict[state]
        else:
            return None


# def printIndices(l):
#     for x in range(BOARD_COLS):
#         tmp = []
#         for y in range(BOARD_ROWS):
#             if (x, y) in l:
#                 tmp.append(1)
#             else:
#                 tmp.append(0)
#         print(tmp)
# print('Printing corners:')
# printIndices(CORNER_INDICES)
#
# print('Near corners')
# printIndices(getNearCornerIndices())
#
# print('Traps:')
# printIndices(getTrapsIndices())
