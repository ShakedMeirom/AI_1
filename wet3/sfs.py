import numpy as np
from sklearn.model_selection import cross_val_score


def cross_validation_score(clf, x, y):
    return (cross_val_score(clf, x, y, cv=4)).mean()


def sfs(x, y, k, clf, score):
    """
    :param x: feature set to be trained using clf. list of lists.
    :param y: labels corresponding to x. list.
    :param k: number of features to select. int
    :param clf: classifier to be trained on the feature subset.
    :param score: utility function for the algorithm, that receives clf, feature subset and labeles, returns a score. 
    :return: list of chosen feature indexes
    """
    x = np.array(x)
    num_samples, num_features = (np.shape(x))
    chosen_features = []
    remaining_features = np.arange(num_features)
    for iteration in range(k):
        best_score = -1
        best_feature = -1
        for feature in remaining_features:
            curr_features = np.array(chosen_features + [feature])
            curr_data = x[:, curr_features]

            # run cross validation on the clf with the current features, and get the mean score:
            curr_score = score(clf, curr_data, y)

            # check whether it is the best score so far:
            if curr_score > best_score:
                best_score = curr_score
                best_feature = feature

        # update the feature lists according to the result:
        chosen_features += [best_feature]
        remaining_features = np.delete(remaining_features, np.argwhere(remaining_features == best_feature))

    assert(len(chosen_features) == k)
    return chosen_features



