##########################################
# No need to edit this file, only run it
# and copy the outputs.
##########################################
from consts import Consts
from astar import AStar
from ways import load_map_from_csv
from busSolvers import GreedyBestFirstSolver
from problems import BusProblem
from costs import L2DistanceCost
from heuristics import L2DistanceHeuristic


#TODO: DOR - the only line here should be : roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
#TODO: I've added the pickle in order to increase speed

#Old:
# roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))

#New:
from time import time
start = time()
import os,pickle
ROADS_ISRAEL_PICKLE = 'roads_israel.pkl'

if os.path.isfile(ROADS_ISRAEL_PICKLE):
    with open(ROADS_ISRAEL_PICKLE,'rb') as fh:
        roads = pickle.load(fh)
else:
    roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
    with open(ROADS_ISRAEL_PICKLE,'wb') as fh:
        pickle.dump(roads, fh)
###############################################

for fileName in ["TLV_5.in", "SDEROT_50.in", "BEER_SHEVA_100.in", "HAIFA_100.in"]:
    print("{}:".format(fileName).ljust(20), flush=True, end="")

    prob = BusProblem.load(Consts.getDataFilePath(fileName))

    mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

    pickingPath = GreedyBestFirstSolver(roads, mapAstar, L2DistanceCost(roads)).solve(prob)

    print("{:.2f}km".format(pickingPath.getDistance() / 1000))
