from . import GreedySolver
import numpy as np

class GreedyBestFirstSolver(GreedySolver):
    def __init__(self, roads, astar, scorer):
        super().__init__(roads, astar, scorer)

    # Find the next state to develop
    def _getNextState(self, problem, currState):
        successors = list(problem.expand(currState))

        minS = successors[0]
        minVal = self._scorer.compute(currState,minS)
        for s in successors[1:]:
            if self._scorer.compute(currState,s) < minVal:
                minVal = self._scorer.compute(currState,s)
                minS = s

        return minS

        # scores = np.asarray([self._scorer.compute(currState,x) for x in successors])
        # bestIdx = scores.argmin()
        # return successors[bestIdx]
