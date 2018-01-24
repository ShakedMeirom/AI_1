import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from collections import Counter
from sklearn.tree import DecisionTreeClassifier

#Consts:

TARGET_LABEL = 'classification'
INPUT_FILE = 'flare.csv'


if __name__ == '__main__':

    classifier = DecisionTreeClassifier(criterion="entropy")

    data = pd.read_csv(INPUT_FILE)

    # print(df.columns)
    target = data[TARGET_LABEL]
    data = data.drop(TARGET_LABEL, axis = 1)
    # scores = cross_val_score(classifier, data, target)
    # print(scores)




    kf = KFold(n_splits= 4, shuffle=False)
    mList = []
    scoreList = []

    for trainIdx, testIdx in kf.split(data):

        tempDataTrain = data.iloc[trainIdx]
        tempTargetTrain = target.iloc[trainIdx]

        tempDataTest = data.iloc[testIdx]
        tempTargetTest = target.iloc[testIdx]

        tree = classifier
        tree.fit(tempDataTrain, tempTargetTrain)
        score = tree.score(tempDataTest, tempTargetTest)



        #Create confusion matrix:
        predicted = list(tree.predict(tempDataTest))
        actual = list(tempTargetTest)
        c = {True: Counter(),
             False: Counter()}

        for i in range(len(predicted)):
            c[actual[i]].update([predicted[i]])
        m = np.empty([2,2])
        m[0][0] = c[True][True]
        m[0][1] = c[True][False]
        m[1][0] = c[False][True]
        m[1][1] = c[False][False]

        mList.append(m)
        scoreList.append(score)


    finalScore = sum(scoreList)/4

    finalM = np.zeros([2,2])
    for m in mList:
        finalM+= m

    print(finalScore)
    print(finalM)







