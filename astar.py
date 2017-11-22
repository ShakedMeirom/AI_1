import numpy as np
import sys

class AStar:
    cost = None
    heuristic = None
    _cache = None
    shouldCache = None

    def __init__(self, heuristic, cost=None, shouldCache=False):
        self.heuristic = heuristic
        self.shouldCache = shouldCache
        self.cost = cost

        # Handles the cache. No reason to change this code.
        if self.shouldCache:
            self._cache = {}

    # Get's from the cache. No reason to change this code.
    def _getFromCache(self, problem):
        if self.shouldCache:
            return self._cache.get(problem)

        return None

    # Get's from the cache. No reason to change this code.
    def _storeInCache(self, problem, value):
        if not self.shouldCache:
            return

        self._cache[problem] = value

    # Run A*
    def run(self, problem):
        # Check if we already have this problem in the cache.
        # No reason to change this code.
        source = problem.initialState
        if self.shouldCache:
            res = self._getFromCache(problem)

            if res is not None:
                return res

        source_h = self.heuristic.estimate(problem, problem.initialState)

        # Initializes the required sets
        closed_set = set()  # The set of nodes already evaluated.
        parents = {}  # The map of navigated nodes.

        # Save the g_score and f_score for the open nodes
        g_score = {source: 0}
        h_score = {source: source_h}
        open_set = {source: source_h}

        developed = 0

        # TODO : Implement astar.
        # Tips:
        # - To get the successor states of a state with their costs, use: problem.expandWithCosts(state, self.cost)
        # - You should break your code into methods (two such stubs are written below)
        # - Don't forget to cache your result between returning it - TODO

        ###### our code ######

        while open_set:
            next = self._getOpenStateWithLowest_f_score(open_set, h_score)
            closed_set.add(next)
            open_set.pop(next)
            if problem.isGoal(next):
                # TODO : VERY IMPORTANT: must return a tuple of (path, g_score(goal), h(I), developed)
                path = self._reconstructParents(parents, next)
                tup = (path, g_score[next], source_h, developed)
                self._storeInCache(problem, tup)
                return tup

            developed += 1
            for s, s_cost in problem.expandWithCosts(next, self.cost):
                new_g = g_score[next] + s_cost
                if s in open_set:
                    # s is in open_set
                    if new_g < g_score[s]:
                        # found better path to s, update accordingly
                        g_score[s] = new_g
                        parents[s] = next
                        open_set[s] = new_g + h_score[s]
                else:
                    if s in closed_set:
                        # s is in closed_set
                        if new_g < g_score[s]:
                            # found better path to s, update accordingly. move s from close to open.
                            g_score[s] = new_g
                            parents[s] = next
                            open_set[s] = new_g + h_score[s]
                            closed_set.remove(s)
                    else:
                        # s is new, add it to open
                        g_score[s] = new_g
                        parents[s] = next
                        s_h = self.heuristic.estimate(problem, s)
                        h_score[s] = s_h
                        open_set[s] = new_g + s_h

        # open_set is empty, there is no solution
        return ([], -1, source_h, developed)

        ######################

    def _getOpenStateWithLowest_f_score(self, open_set, h_score):




        minList =[]

        for s in open_set:
            if minList == []:
                minList = [s]
                fMin = open_set[s]
            else:
                curF = open_set[s]
                if curF < fMin:
                    fMin = curF
                    minList = [s]
                elif curF == fMin:
                    minList.append(s)

        sMin = minList.pop()
        hMin = h_score[sMin]

        for s in minList:
            if h_score[s] < hMin:
                hMin = h_score[s]
                sMin = s

        return sMin


    # create a list of states from a given state by its parent and so on
    def _reconstructParents(self, parents:dict, state):

        # cont = True
        parents_list = []
        # parents_list.append(state)
        # while cont:
        #     if state in parents:
        #         s_parent = parents[state]
        #         parents_list.append(s_parent)
        #         state = s_parent
        #     else:
        #         cont = False
        # return parents_list

        while state in parents:
            parents_list.append(state)



            state = parents[state]

        parents_list.reverse()
        return parents_list









