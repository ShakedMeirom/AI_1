import os,sys
import pandas as pd
import numpy as np
from collections import Counter

FILE = 'temp.csv'

c = Counter()

with open(FILE,'r') as fh:
    data = fh.readlines()


data = [x.rstrip('\n') for x in data]
print(len(data))
c.update(data)

totalOhShit = 0
lost = 0
def findAlternative(c, x):
    global totalOhShit
    global lost
    newX = None
    if x.endswith('False'):
        newX = x.replace('False','True')

    if x.endswith('True'):
        newX = x.replace('True', 'False')

    if newX is None:
        return

    if newX in c:
        myVal = c[x]
        theirVal = c[newX]

        if (theirVal > myVal):
            lost+= myVal
        if (theirVal == myVal):
            totalOhShit+= myVal

for x in c.keys():
    findAlternative(c,x)

totalOhShit/=2
totalLost = lost + totalOhShit

print('Total data:', len(data))
print('Total lost:', totalLost )
print('Lost:', 1 - totalLost/len(data))
