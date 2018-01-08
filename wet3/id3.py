import pandas as pd
import sklearn
import numpy as np
from copy import copy

INPUT_FILE = r'flare.csv'


class Node:

    def __init__(self):

        self.feature = None
        self.pRight = None
        self.pLeft = None
        self.prediction = None # Only for leafs

    def isLeaf(self):
        return self.pRight is None and self.pLeft is None


#Right subtree if feature evaluates to true, left if feature evaluates to false

class ID3DecisionTreeClassifier:



    def __init__(self):
        self.tree = None


    #Data is a dataframe where each column is a feature, the classification of
    #data[i] is target[i]
    def fit(self, data, target):

        features = list(data.columns)
        self.tree = createTree(data, target, features)

    def predict(self, vals):
        res = []
        for i in range(vals.shape[0]):
            currentData = vals.iloc[[i]]
            res.append(self._getPrediction(currentData, self.tree))

        return res

    def _getPrediction(self, data, tree ):


        if tree.isLeaf():
            assert tree.prediction is not None
            return tree.prediction


        assert data[tree.feature].size == 1
        val  = data[tree.feature].iloc[0]
        if val == True:
            #TODO: DOR - what happenes if pRight/left is None?
            return self._getPrediction(data, tree.pRight)
        else:
            return self._getPrediction(data, tree.pLeft)

    def score(self, data, target):
        res = self.predict(data)

        correct = 0
        for i in range(len(res)):
            if res[i] == target.iloc[i]:
                correct+=1
        return correct/ len(res)



def createTree(data, target, features):


        #True is the default value
        if target.size == 0:
            node = Node()
            node.prediction = True
            return node
        
        majorityClass = target.value_counts().index[0]



        #TODO  - what happens when there are no more features?
        if not features or all(target == majorityClass):
            node = Node()
            node.prediction = majorityClass

            return node

        f = selectFeature(data, target, features)
        features.remove(f)
        rightData, rightTarget = createSubTreeData(f, True, data, target)
        leftData, leftTarget = createSubTreeData(f, False, data, target)


        node = Node()
        node.feature = f
        node.pRight = createTree(rightData, rightTarget, features)
        node.pLeft = createTree(leftData, leftTarget, features)

        return node


#Return tuple of (data, target), whereas data[feature] == value
def createSubTreeData(feature, value, data, target):

        newTarget = target[data[feature] == value]
        newData = data[data[feature] == value]

        return newData, newTarget


def selectFeature(data, target, features):

    informationGainList =\
        np.asarray([informationGain(data, target, f) for f in features])
    return features[informationGainList.argmax()]

def informationGain(data, target, feature):

    currentEntropy = getEntropy(data, target)
    childrenEntropy = 0
    ec = data.shape[0]

    featureDomain = data[feature].unique()

    for v in featureDomain:
        tempData, tempTarget = createSubTreeData(feature, v, data, target)
        ev = tempData.shape[0]
        childrenEntropy += (ev/ec)*getEntropy(tempData, tempTarget)

    return currentEntropy - childrenEntropy

def getEntropy(data, target):

    entropy = 0

    classes = list(target.unique())
    for c in classes:
        ec = data[target == c].shape[0]
        pc = ec/data.shape[0]

        if pc > 0:
            entropy -= pc*np.log2(pc)

    return entropy







