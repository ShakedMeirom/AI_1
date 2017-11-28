import numpy as np
from matplotlib import pyplot as plt

X = np.array([400,900,390,1000,550])

def calcPorbabilty(l, t, n):
    elementsNum = min(n, len(l))
    l = l[:elementsNum] #take maximum n elements


    minVal = min(l)
    pl = [np.power(x,-1./t)/minVal for x in l]
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
    plt.show()


