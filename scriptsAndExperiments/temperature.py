import numpy as np
from matplotlib import pyplot as plt

X = np.array([400,900,390,1000,550])

def calcPorbabilty(X_arr, t, n):
    bestX = []
    if len(X_arr) <= n:
        bestX = X_arr
    else:
        X_arr = np.asarray(X_arr)
        best_X_indexes = np.argpartition(X_arr, n) #finds the N smallest elements in X
        bestX = X_arr[best_X_indexes[:n]]

    minVal = min(bestX)
    maxBestVal = max(bestX)
    pl = []
    for x in X_arr:
        if x > maxBestVal:
            pl.append(0)
        else:
            pl.append(np.power(x/float(minVal),-1./t))
    plSum = sum(pl)

    if plSum != 0:
        pl = [x/plSum for x in pl]
    else:
        pl = [1/len(pl)]*len(pl) # uniform

    return pl

#ex 17 - plot graph:


tList = np.linspace(0.01, 5 , 100)
funcsDict = {}
for x in X:
    funcsDict[x] = []

for t in tList:
    res = calcPorbabilty(X, t, 5)

    for x, r in zip(X, res):
        funcsDict[x].append(r)

if __name__ == '__main__':

    for number, f in funcsDict.items():
        plt.plot(tList, f, label = str(number))
    plt.legend(loc = 'upper right')
    plt.title('probability as a function of the temperature')
    plt.xlabel('T')
    plt.ylabel('P')
    plt.grid()
    plt.show()


