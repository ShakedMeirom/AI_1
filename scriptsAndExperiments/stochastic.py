from consts import Consts
from astar import AStar
from ways import load_map_from_csv
from busSolvers import GreedyBestFirstSolver, GreedyStochasticSolver
from problems import BusProblem
from costs import L2DistanceCost
from heuristics import L2DistanceHeuristic
import numpy as np

#TODO: DOR: Change repeats back to 150
REPEATS = 150
# REPEATS = 10

# Load the files
roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
prob = BusProblem.load(Consts.getDataFilePath("HAIFA_100.in"))

mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

scorer = L2DistanceCost(roads)

# Run the greedy solver
pickingPath = GreedyBestFirstSolver(roads, mapAstar, scorer).solve(prob)
greedyDistance = pickingPath.getDistance() / 1000
print("Greedy solution: {:.2f}km".format(greedyDistance))

# Run the stochastic solver #REPATS times
solver = GreedyStochasticSolver(roads, mapAstar, scorer,
                                Consts.STOCH_INITIAL_TEMPERATURE,
                                Consts.STOCH_TEMPERATURE_DECAY_FUNCTION,
                                Consts.STOCH_TOP_SCORES_TO_CONSIDER)
#TODO: DOR - remove pickle
#TODO: DOR - at the moment we're getting wrong results.
#stochastic returns distance of about 4000, and non stochastic returns 1329

#Add pickle to save time:
import os
import pickle
RESULTS_PICKLE_NAME = 'stochastic_greedy_'+str(REPEATS)+'.pkl'

if os.path.isfile(RESULTS_PICKLE_NAME):
    with open(RESULTS_PICKLE_NAME,'rb') as fh:
        results = pickle.load(fh)
else:

    results = np.zeros((REPEATS,))
    print("Stochastic repeats:")
    for i in range(REPEATS):
        print("{}..".format(i+1), end=" ", flush=True)
        results[i] = solver.solve(prob).getDistance() / 1000

    print("\nDone!")
    with open(RESULTS_PICKLE_NAME,'wb') as fh:
        pickle.dump(results, fh)



#Create results for plotting (in order to make in monotonic)
plotResults = []
plotResults.append(results[0])
best = plotResults[0]

for r in results[1:]:
    if r < best:
        best = r
    plotResults.append(best)

greedyResult = [greedyDistance]*len(plotResults)

# TODO : Part1 - Plot the diagram required in the instructions
from matplotlib import pyplot as plt

iterations = range(1, len(results)+1)
plt.plot(iterations, plotResults, label = 'stochastic')
plt.plot(iterations, greedyResult, label = 'non stochastic')
plt.title('Greedy Stochastic algorithm performance')
plt.xlabel('iteration')
plt.ylabel('distance')
plt.legend(loc = 'upper right')
plt.show()



#TODO: DOR: currently the code runs awfully slow, the main time consumption comes from aStar.
#Need to profile aStar.run function


# # TODO : Part2 - Remove the exit and perform the t-test
resultsArr = np.asarray(results)
variance = resultsArr.var()
mean = resultsArr.mean()

# raise NotImplementedError



