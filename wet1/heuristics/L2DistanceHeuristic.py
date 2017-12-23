from . import Heuristic
from ways.tools import compute_distance

# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        # TODO : Return the correct distance
        coord1 = state.coordinates
        coord2 = problem.target.coordinates

        return compute_distance(coord1, coord2)

