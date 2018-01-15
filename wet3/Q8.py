from parse_data import *
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


if __name__ == '__main__':
    # parse data:
    x, y = parse_data_to_lists()

    # split the data to train and test:
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.25)

    # train a Decision Tree without pruning:
    ID3 = DecisionTreeClassifier(criterion="entropy")
    ID3.fit(xTrain, yTrain)

    # check the accuracy:
    print("ID3 accuracy, without pre-pruning, is: ", ID3.score(xTest, yTest))

    # train a Decision Tree with pre-pruning:
    ID3_pre_pruning = DecisionTreeClassifier(criterion="entropy", min_samples_split=21)
    ID3_pre_pruning.fit(xTrain, yTrain)

    # check the accuracy:
    print("ID3 accuracy, with pre-pruning, is: ", ID3_pre_pruning.score(xTest, yTest))

