import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import time
import copy
import math
import numpy as np

#Consts:
LAST_COL = BOARD_COLS - 1
LAST_ROW = BOARD_ROWS - 1
CORNER_INDICES = [(LAST_COL, 0), (0, 0), (LAST_COL, LAST_ROW), (0, LAST_ROW)]



#Utils:
# "near corners" are squares that allow direct access to corners
def getNearCornerIndices():

    nearCornerIndices = []

    for x,y in CORNER_INDICES:

        if x == 0:
            nearCornerIndices.append((1,y))

        if y == 0:
            nearCornerIndices.append((x,1))

        if x == LAST_COL:
            nearCornerIndices.append((LAST_COL-1, y))

        if y == LAST_ROW:
            nearCornerIndices.append((x, LAST_ROW -1))

    diagonalToCorner = [(LAST_COL-1, 1),(LAST_COL -1, LAST_ROW-1),
                        (1, LAST_ROW -1), (1,1)]

    nearCornerIndices += diagonalToCorner
    return nearCornerIndices

#Traps are squares thata allow access to "near corner" squares
def getTrapsIndices():

    nearCornerIndices = getNearCornerIndices()
    trapIndices = []

    for x,y in nearCornerIndices:

        if x == 1:
            trapIndices.append((2,y))

        if y == 1:
            trapIndices.append((x,2))

        if x == LAST_COL-1:
            trapIndices.append((LAST_COL-2, y))

        if y == LAST_ROW-1:
            trapIndices.append((x, LAST_ROW -2))

    diagonalToNearCorner = [(LAST_COL-2, 2),(LAST_COL -2, LAST_ROW-2),
                        (2, LAST_ROW -2), (2,2)]

    trapIndices += diagonalToNearCorner

    return trapIndices



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

    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

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

    def discs_diff(self, state):
        my_u = 0
        op_u = 0
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if state.board[x][y] == self.color:
                    my_u += 1
                if state.board[x][y] == OPPONENT_COLOR[self.color]:
                    op_u += 1

        if my_u == 0:
            # I have no tools left
            return -INFINITY
        elif op_u == 0:
            # The opponent has no tools left
            return INFINITY
        else:
            return my_u - op_u

    def opponent_moves(self, state):
        return len(state.get_possible_moves())

    def heuristic(self, state):
        if len(state.get_possible_moves()) == 0:
            return INFINITY if state.curr_player != self.color else -INFINITY

        weightsParamsTupleList = [
            (1, self.discs_diff(state)),
            (0.25, self.opponent_moves(state)),
            (5, self.countCorners(state, self.color)),
            (-1.5, self.countNearCorners(state, self.color)),
            (0.5, self.countTraps(state, self.color)),
            (1, self.countEdges(state, self.color))]


        heuristic_value = 0
        for weight, param in weightsParamsTupleList:
            heuristic_value += weight * param

        return heuristic_value

    #Return how many corners belongs to color
    def countCorners(self, state, color):


        cornersVal = [state.board[x][y] for x,y in CORNER_INDICES]

        cornersCount = sum([x == color for x in cornersVal])
        # print('Corners count:', cornersCount)
        return cornersCount


    # "near corners" are squares that allow direct access to corners
    def countNearCorners(self, state, color):


        nearCornerIndices = getNearCornerIndices()
        nearCornersVal = [state.board[x][y] for x,y in nearCornerIndices]

        nearCornersCount = sum([x == color for x in nearCornersVal])
        # print('Near corners count:', nearCornersCount)
        return nearCornersCount


    def countTraps(self, state, color):

        trapIndices = getTrapsIndices()
        trapVals = [state.board[x][y] for x,y in trapIndices]

        trapsCount = sum([x == color for x in trapVals])
        # print('Traps count:', trapsCount)
        return trapsCount

    def countEdges(self, state, color):

        count = 0
        nearCorners = getNearCornerIndices()
        traps = getTrapsIndices()

        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if state.board[x][y] == color and \
                        (x == 0 or x == LAST_COL or y == 0 or y == LAST_ROW) and\
                        ((x, y) not in nearCorners and
                         (x, y) not in traps and
                         (x, y) not in CORNER_INDICES):
                    count += 1
        # print('Edges count:', count)
        return count

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better')

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
