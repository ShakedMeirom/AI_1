from sfs import *
from parse_data import *
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


if __name__ == '__main__':
    # parse data:
    x, y = parse_data_to_lists()

    # split the data to train and test:
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.25)

    # train a knn classifier with 5 neighbors
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(xTrain, yTrain)

    # check the accuracy:
    print("KNN accuracy, without feature selection, is: ", knn.score(xTest, yTest))

    # select 8 features for the knn:
    knn_selected = KNeighborsClassifier(n_neighbors=5)

    num_chosen_features = 8
    chosen_features = sfs(xTrain, yTrain, num_chosen_features, knn_selected, cross_validation_score)
    print(chosen_features)

    # chose only the selected feature from the data, and train the knn with them:
    train_data_selected = (np.array(xTrain))[:, chosen_features]
    knn_selected.fit(train_data_selected, yTrain)

    # check the accuracy:
    test_data_selected = (np.array(xTest))[:, chosen_features]
    print("KNN accuracy, with feature selection, is: ", knn_selected.score(test_data_selected, yTest))


