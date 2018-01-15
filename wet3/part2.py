from sfs import *
from parse_data import *
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

if __name__ == '__main__':

    # parse data:
    x, y = parse_data_to_lists()

    # in order to get the mean accuracy of each classifier, calculate the accuracy over 10 iterations of fit and score:

    all_accuracies = {"knn": [], "knn_selected": [], "ID3": [], "ID3_pre_pruning": []}

    for i in range(10):
        # split the data to train and test:
        xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.25)


        ########## KNN ###############
        # train a knn classifier with 5 neighbors
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(xTrain, yTrain)

        # check the current accuracy and add to the list of accuracies of this classifier:
        all_accuracies["knn"].append(knn.score(xTest, yTest))

        ########## KNN with selected features ###############
        # select 8 features for the knn:
        knn_selected = KNeighborsClassifier(n_neighbors=5)

        num_chosen_features = 8
        chosen_features = sfs(xTrain, yTrain, num_chosen_features, knn_selected, cross_validation_score)

        # chose only the selected feature from the data, and train the knn with them:
        train_data_selected = (np.array(xTrain))[:, chosen_features]
        knn_selected.fit(train_data_selected, yTrain)

        # check the current accuracy and add to the list of accuracies of this classifier:
        test_data_selected = (np.array(xTest))[:, chosen_features]
        all_accuracies["knn_selected"].append(knn_selected.score(test_data_selected, yTest))

        ########## ID3 ###############
        # train a Decision Tree without pruning:
        ID3 = DecisionTreeClassifier(criterion="entropy")
        ID3.fit(xTrain, yTrain)

        # check the current accuracy and add to the list of accuracies of this classifier:
        all_accuracies["ID3"].append(ID3.score(xTest, yTest))

        ########## ID3 with pre-pruning ###############
        # train a Decision Tree with pre-pruning:
        ID3_pre_pruning = DecisionTreeClassifier(criterion="entropy", min_samples_split=21)
        ID3_pre_pruning.fit(xTrain, yTrain)

        # check the current accuracy and add to the list of accuracies of this classifier:
        all_accuracies["ID3_pre_pruning"].append(ID3_pre_pruning.score(xTest, yTest))

    # calculate and print mean accuracies:
    print("KNN mean accuracy, without feature selection, is: ", np.mean(all_accuracies["knn"]))
    print("KNN mean accuracy, with feature selection, is: ", np.mean(all_accuracies["knn_selected"]))
    print("ID3 mean accuracy, without pre-pruning, is: ", np.mean(all_accuracies["ID3"]))
    print("ID3 mean accuracy, with pre-pruning, is: ", np.mean(all_accuracies["ID3_pre_pruning"]))


