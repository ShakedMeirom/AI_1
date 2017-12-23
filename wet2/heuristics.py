import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS


LAST_COL = BOARD_COLS - 1
LAST_ROW = BOARD_ROWS - 1
CORNER_INDICES = [(LAST_COL, 0), (0, 0), (LAST_COL, LAST_ROW), (0, LAST_ROW)]

def smart_heuristic(state, color):
    if len(state.get_possible_moves()) == 0:
        diff = discs_diff(state, color)
        if diff > 0:
            return INFINITY
        elif diff < 0:
            return -INFINITY
        else:
            return 0

    weightsParamsTupleList = [
        (1, discs_diff(state, color)),
        (0.25, opponent_moves(state)),
        (5, countCorners(state, color)),
        (-1.5, countNearCorners(state, color)),
        (0.5, countTraps(state, color)),
        (1, countEdges(state, color))]


    heuristic_value = 0
    for weight, param in weightsParamsTupleList:
        heuristic_value += weight * param

    return heuristic_value



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


def discs_diff(state, color):
    my_u = 0
    op_u = 0
    for x in range(BOARD_COLS):
        for y in range(BOARD_ROWS):
            if state.board[x][y] == color:
                my_u += 1
            if state.board[x][y] == OPPONENT_COLOR[color]:
                op_u += 1

    if my_u == 0:
        # I have no tools left
        return -INFINITY
    elif op_u == 0:
        # The opponent has no tools left
        return INFINITY
    else:
        return my_u - op_u


def opponent_moves(state):
    return len(state.get_possible_moves())


#Return how many corners belongs to color
def countCorners(state, color):


    cornersVal = [state.board[x][y] for x,y in CORNER_INDICES]

    cornersCount = sum([x == color for x in cornersVal])
    # print('Corners count:', cornersCount)
    return cornersCount


# "near corners" are squares that allow direct access to corners
def countNearCorners(state, color):


    nearCornerIndices = getNearCornerIndices()
    nearCornersVal = [state.board[x][y] for x,y in nearCornerIndices]

    nearCornersCount = sum([x == color for x in nearCornersVal])
    # print('Near corners count:', nearCornersCount)
    return nearCornersCount


def countTraps(state, color):

    trapIndices = getTrapsIndices()
    trapVals = [state.board[x][y] for x,y in trapIndices]

    trapsCount = sum([x == color for x in trapVals])
    # print('Traps count:', trapsCount)
    return trapsCount

def countEdges(state, color):

    count = 0
    nearCorners = getNearCornerIndices()
    traps = getTrapsIndices()

    for x in range(BOARD_COLS):
        for y in range(BOARD_ROWS):
            if state.board[x][y] == color and \
                    (x == 0 or x == LAST_COL or y == 0 or y == LAST_ROW) and \
                    ((x, y) not in nearCorners and
                             (x, y) not in traps and
                             (x, y) not in CORNER_INDICES):
                count += 1
    # print('Edges count:', count)
    return count
