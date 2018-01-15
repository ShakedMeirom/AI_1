import id3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

TARGET_LABEL = 'classification'
INPUT_FILE = 'flare.csv'

class overFittedTree(id3.ID3DecisionTreeClassifier):
    @staticmethod
    def selectFeature(data, target, features):
        return super().selectFeature(data, target, features)






if __name__ == '__main__':

    classifier = id3.ID3DecisionTreeClassifier

    data = pd.read_csv(INPUT_FILE)

    # print(df.columns)
    target = data[TARGET_LABEL]
    data = data.drop(TARGET_LABEL, axis = 1)

    xTrain, xTest, yTrain, yTest = train_test_split(data, target, test_size= 0.25)

    tree = classifier()
    tree.fit(xTrain, yTrain)

    res = tree.predict(xTrain)

    print('Accuracy on trainning:', tree.score(xTrain, yTrain))
    print('Accuracy on test:', tree.score(xTest, yTest))

