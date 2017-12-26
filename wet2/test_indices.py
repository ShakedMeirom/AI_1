from heuristics import *
import numpy as np

def printIndices(l):
    for x in range(BOARD_COLS):
        tmp = []
        for y in range(BOARD_ROWS):
            if (x, y) in l:
                tmp.append(1)
            else:
                tmp.append(0)
        print(tmp)

print([position for sublist in NEAR_CORNER_INDICES for position in sublist])

print('Printing corners:')
printIndices(CORNER_INDICES)

print('Near corners')
printIndices([position for sublist in NEAR_CORNER_INDICES for position in sublist])

print('Traps:')
printIndices([position for sublist in TRAPS_INDICES for position in sublist])
