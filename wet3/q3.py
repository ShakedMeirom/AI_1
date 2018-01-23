import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from parse_data import *

TARGET_LABEL = 'classification'
INPUT_FILE = 'flare.csv'

if __name__ == '__main__':

    # parse data:
    x, y = parse_data_to_lists()

    # split the data to train and test:
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.25)

    ######### Over-Fit ####################
    # train an over-fitted Decision Tree:
    ID3_overfit = DecisionTreeClassifier(criterion="entropy")
    ID3_overfit.fit(xTrain, yTrain)

    # check the accuracy of the over-fitted tree:
    print("ID3 over-fit version: accuracy on train, is: ", ID3_overfit.score(xTrain, yTrain))

    ######### Under-Fit ####################
    # train an under-fitted Decision Tree:
    ID3_underfit = DecisionTreeClassifier(criterion="entropy", max_depth=1)
    ID3_underfit.fit(xTrain, yTrain)

    # check the accuracy of the over-fitted tree:
    print("ID3 under-fit version accuracy on train, is: ", ID3_underfit.score(xTrain, yTrain))
