import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import scripts
from Reversi.board import  GameState
from copy import deepcopy
import numpy as np

LAST_COL = BOARD_COLS - 1
LAST_ROW = BOARD_ROWS - 1
CORNER_INDICES = [(LAST_COL, 0), (0, 0), (LAST_COL, LAST_ROW), (0, LAST_ROW)]
TRAPS_INDICES = [[(0,2), (2,0), (2,2)],
                 [(LAST_COL-2, 0), (LAST_COL, 2), (LAST_COL-2, 2)],
                 [(0, LAST_ROW-2), (2,LAST_ROW), (2,LAST_ROW-2)],
                 [(LAST_COL,LAST_ROW-2), (LAST_COL-2, LAST_ROW), (LAST_COL-2,LAST_ROW-2)]]

NEAR_CORNER_INDICES = [[(0,1), (1,0), (1,1)],
                       [(LAST_COL-1, 0), (LAST_COL, 1), (LAST_COL-1, 1)],
                       [(0, LAST_ROW-1), (1,LAST_ROW), (1,LAST_ROW-1)],
                       [(LAST_COL,LAST_ROW-1), (LAST_COL-1, LAST_ROW), (LAST_COL-1,LAST_ROW-1)]]


def _find_winner(state, color):
    diff = discs_diff(state, color)
    if diff > 0:
        return INFINITY
    elif diff < 0:
        return -INFINITY
    else:
        return 0


def _calc_heuristic_value(weightsParamsTupleList):
    heuristic_value = 0
    for weight, param in weightsParamsTupleList:
        heuristic_value += weight * param

    return heuristic_value

def flatten_list(deep_list):
    return [position for sublist in deep_list for position in sublist]


def smart_heuristic(state, color):
    if len(state.get_possible_moves()) == 0:
        return _find_winner(state, color)

    weightsParamsTupleList = [
        (1, discs_diff(state, color)),
        (0.25, opponent_moves(state, color)),
        (6, countCorners(state, color)),  # 5
        (-0.5, countNearCorners(state, color)),  # -1.5
        (0.4, countTraps(state, color)),
        (0.25, countEdges(state, color)),  # 1
        (0.5, assessStable(state, color))]  # 1

    return _calc_heuristic_value(weightsParamsTupleList)


def safe_heuristic(state, color):
    if len(state.get_possible_moves()) == 0:
        return _find_winner(state, color)

    weightsParamsTupleList = [
        (1, discs_diff(state, color)),
        (0.25, opponent_moves(state, color)),
        (5, countCorners(state, color))]

    return _calc_heuristic_value(weightsParamsTupleList)


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

    trapIndices = [(0,2), (2,0), (LAST_COL-2, 0), (0, LAST_COL-2)]
    diagonalToNearCorner = [(LAST_COL-2, 2),(LAST_COL -2, LAST_ROW-2),
                            (2, LAST_ROW -2), (2,2)]

    trapIndices += diagonalToNearCorner

    return trapIndices


def discs_diff(state, color):
    # my_u = 0
    # op_u = 0
    board_arr = np.asarray(state.board)
    my_u = len(np.where(board_arr == color))
    op_u = len(np.where(board_arr == OPPONENT_COLOR[color]))
    # for x in range(BOARD_COLS):
    #     for y in range(BOARD_ROWS):
    #         if state.board[x][y] == color:
    #             my_u += 1
    #         if state.board[x][y] == OPPONENT_COLOR[color]:
    #             op_u += 1

    if my_u == 0:
        # I have no tools left
        return -INFINITY
    elif op_u == 0:
        # The opponent has no tools left
        return INFINITY
    else:
        return my_u - op_u


def opponent_moves(state, color):
    if state.curr_player == color:
        return len(state.get_possible_moves())
    else:
        return -len(state.get_possible_moves())


#Return how many corners belongs to color
def countCorners(state, color):

    cornersVal = [state.board[x][y] for x,y in CORNER_INDICES]

    cornersCount = sum([x == color for x in cornersVal]) - sum([x == OPPONENT_COLOR[color] for x in cornersVal])
    # print('Corners count:', cornersCount)
    return cornersCount


def kth_diag_indices(mat, k):
    k = 7 - k
    rows, cols = np.diag_indices_from(mat)
    if k < 0:
        return rows[-k:], cols[:k]
    elif k > 0:
        return rows[:-k], cols[k:]
    else:
        return rows, cols

def kth_diag_colors(state, mat, color, k):
    curr_stable_indices = []
    all_diag = True
    diag_indices = kth_diag_indices(mat,k)
    diag_colors = (mat[diag_indices])
    for i in range(1,k+1):
        if diag_colors.item(i) == color:
            curr_stable_indices.append((diag_indices[0][i],diag_indices[1][i]))
        else:
            all_diag = False
    return curr_stable_indices, all_diag

def assessStable(state, color):
    stable_indices = []
    mat = np.matrix(state.board)
    if state.board[0][0] == color:
        for k in range(1,7):
            curr_stable_indices, all_diag = kth_diag_colors(state, np.flip(mat,1), color, k)
            stable_indices += curr_stable_indices
            if not all_diag:
                break

    if state.board[0][LAST_COL] == color:
        for k in range(1, 7):
            curr_stable_indices, all_diag = kth_diag_colors(state, mat, color, k)
            stable_indices += curr_stable_indices
            if not all_diag:
                break

    if state.board[LAST_ROW][LAST_COL] == color:
        for k in range(1, 7):
            curr_stable_indices, all_diag = kth_diag_colors(state, np.flip(np.flip(mat,0),1), color, k)
            stable_indices += curr_stable_indices
            if not all_diag:
                break

    if state.board[LAST_ROW][LAST_COL] == color:
        for k in range(1, 7):
            curr_stable_indices, all_diag = kth_diag_colors(state, np.flip(mat,0), color, k)
            stable_indices += curr_stable_indices
            if not all_diag:
                break

    return len(set(stable_indices))


# "near corners" are squares that allow direct access to corners
def countNearCorners(state, color):

    #nearCornerIndices = getNearCornerIndices()
    nearEmptyCornersVal = []
    nearMyCornersVal = []
    for idx, corner in enumerate(CORNER_INDICES):
        if state.board[corner[0]][corner[1]] == EM:
            nearEmptyCornersVal += [state.board[x][y] for x,y in NEAR_CORNER_INDICES[idx]]
        elif state.board[corner[0]][corner[1]] == color:
            nearMyCornersVal += [state.board[x][y] for x,y in NEAR_CORNER_INDICES[idx]]

    nearCornersCount = sum([x == color for x in nearEmptyCornersVal]) - sum([x == color for x in nearMyCornersVal])
    # print('Near corners count:', nearCornersCount)
    return nearCornersCount


def countTraps(state, color):

    #trapIndices = getTrapsIndices()
    trapVals = []
    for idx, corner in enumerate(CORNER_INDICES):
        if state.board[corner[0]][corner[1]] == EM:
            trapVals += [state.board[x][y] for x,y in TRAPS_INDICES[idx]]

    trapsCount = sum([x == color for x in trapVals])
    # print('Traps count:', trapsCount)
    return trapsCount

def countEdges(state, color):

    count = 0
    #nearCorners = getNearCornerIndices()
    #traps = getTrapsIndices()

    notEdges = flatten_list(TRAPS_INDICES) + flatten_list(NEAR_CORNER_INDICES) + flatten_list(CORNER_INDICES)


    for x in range(BOARD_COLS):
        for y in range(BOARD_ROWS):
            if state.board[x][y] == color and \
                    (x == 0 or x == LAST_COL or y == 0 or y == LAST_ROW) and \
                    ((x, y) not in notEdges):
                count += 1
    # print('Edges count:', count)
    return count



############Opening related utils:#################################



def getPartialOpeningsDict():

    #d holds
    l = scripts.createOpeningsDict()

    # For each partial board state add a board to the hash with the next move.
    openings = {}
    for val, _ in l:
        game = GameState()
        bookX, bookY = val[1], val[2]
        openings[deepcopy(game)] = transformBookToOurCoordinates(bookX, bookY)

        for i in range(0, len(val)-3, 3):
            bookX = val[i+1]
            bookY = val[i+2]

            moveX, moveY = transformBookToOurCoordinates(val[i+4], val[i+5])
            game.perform_move(*transformBookToOurCoordinates(bookX, bookY))
            openings[deepcopy(game)] = (moveX, moveY)

    return openings

def transformBookToOurCoordinates(x, y):

    BOOK_X_TO_OUR_Y = {
        'a': 7,
        'b': 6,
        'c': 5,
        'd': 4,
        'e': 3,
        'f': 2,
        'g': 1,
        'h': 0
    }

    BOOK_Y_TO_OUR_X = {
        '1': 0,
        '2': 1,
        '3': 2,
        '4': 3,
        '5': 4,
        '6': 5,
        '7': 6,
        '8': 7
    }

    return BOOK_Y_TO_OUR_X[y], BOOK_X_TO_OUR_Y[x]
