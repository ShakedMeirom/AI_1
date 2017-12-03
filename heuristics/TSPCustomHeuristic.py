from heuristics import Heuristic
from ways.tools import compute_distance
# TODO : Implement as explained in the instructions
class TSPCustomHeuristic(Heuristic):
    _distMat = None
    _junctionToMatIdx = None

    # TODO : You can add parameters if you need them
    def __init__(self, roads, initialState):
        self._roads = roads
        super().__init__()

    # Estimate heuristically the minimal cost from the given state to the problem's goal
    def estimate(self, problem, state):
        stateCoordinates = self._roads[state.junctionIdx].coordinates
        waitingSourceCoordinates = [self._roads[x[0]].coordinates for x in state.waitingOrders]
        distances = [compute_distance(stateCoordinates,x) for x in waitingSourceCoordinates]
        if distances: #if list is not empty
            return max(distances)
        else:
            return 0

