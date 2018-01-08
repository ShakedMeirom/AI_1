import pandas as pd
import id3
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

#Consts:

TARGET_LABEL = 'classification'
INPUT_FILE = 'flare.csv'


if __name__ == '__main__':

    classifier = id3.ID3DecisionTreeClassifier

    data = pd.read_csv(INPUT_FILE)

    # print(df.columns)
    target = data[TARGET_LABEL]
    data = data.drop(TARGET_LABEL, axis = 1)
    # scores = cross_val_score(classifier, data, target)
    # print(scores)




    kf = KFold(n_splits= 4, shuffle=False)
    for trainIdx, testIdx in kf.split(data):
        tempDataTrain = data.iloc[trainIdx]
        tempTargetTrain = target.iloc[trainIdx]

        tempDataTest = data.iloc[testIdx]
        tempTargetTest = target.iloc[testIdx]

        tree = classifier()
        tree.fit(tempDataTrain, tempTargetTrain)
        score = tree.score(tempDataTest, tempTargetTest)

        print('Score is:', score)




