import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeRegressor

# This file contains the feature data
# The first two columns of a row are (source_user_id, destination_id)
# The third column is the personalized pagerank score between the nodes
# The last column of the row can be either 1 or 0. 1 if the edge is known to exist, 0 otherwise.
# The rest of the columns from fourth to last -1 are features on that edge.
FILENAME = "features_data.csv"

# Read the data from the file into numpy array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data

def plot_feature_importance(feature_importance, indices, stddev, filename):
    # Plot the feature importances of the forest
    import pylab as pl
    pl.figure()
    pl.title("Feature importances")
    pl.bar(range(len(feature_importance)), feature_importance[indices],
           color="r", yerr=stddev[indices], align="center")
    pl.xticks(range(len(feature_importance)), indices)
    pl.xlim([-1, len(feature_importance)])
    pl.savefig(filename + ".png")

def run_random_forest(data, _max_depth):
    (feature_train, feature_test, label_train, label_test) = train_test_split(data[:, 0:-1], data[:, -1].astype(int),
                                                                              test_size=0.25)

    # TODO: Vary Number of Estimators
    rfc = RandomForestClassifier(n_estimators=500, criterion='gini', max_depth=_max_depth, max_features='auto',
                                     bootstrap=True, oob_score=True, n_jobs=1)
    rfc.fit(feature_train, label_train)
    training_error = rfc.score(feature_train, label_train)
    cross_validation_score = cross_val_score(rfc, feature_train, label_train, cv=10)
    testing_error = rfc.score(feature_test, label_test)
    out_of_bag_error = rfc.oob_score_

    print "Random Forest Results for Max Depth:", _max_depth
    print "Training Accuracy:", training_error
    print "10-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)" % (cross_validation_score.mean(), cross_validation_score.std() * 2)
    print "Testing Accuracy:", testing_error
    print "Out of Bag Accuracy:", out_of_bag_error

    feature_importance = rfc.feature_importances_
    stddev = np.std([tree.feature_importances_ for tree in rfc.estimators_], axis=0)
    indices = np.argsort(feature_importance)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(len(feature_importance)):
        print("%d. feature %d (%f)" % (f + 1, indices[f], feature_importance[indices[f]]))

    plot_feature_importance(feature_importance, indices, stddev, "random-forest-feature-importance-depth-" + str(_max_depth))

def run_gradient_boosting_classifier(data, _max_depth):
    (feature_train, feature_test, label_train, label_test) = train_test_split(data[:, 0:-1], data[:, -1].astype(int),
                                                                              test_size=0.25)
    # TODO: Vary Number of Estimators and Learning Rate
    gbc = GradientBoostingClassifier(learning_rate=0.1, n_estimators=300, max_depth=_max_depth)
    gbc.fit(feature_train, label_train)
    training_error = gbc.score(feature_train, label_train)
    cross_validation_score = cross_val_score(gbc, feature_train, label_train, cv=10)
    testing_error = gbc.score(feature_test, label_test)

    print "Random Forest Results for Max Depth:", _max_depth
    print "Training Accuracy:", training_error
    print "10-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)" % (cross_validation_score.mean(), cross_validation_score.std() * 2)
    print "Testing Accuracy:", testing_error

    feature_importance = gbc.feature_importances_
    stddev = np.std([tree[0].feature_importances_ for tree in gbc.estimators_], axis=0)
    indices = np.argsort(feature_importance)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(len(feature_importance)):
        print("%d. feature %d (%f)" % (f + 1, indices[f], feature_importance[indices[f]]))

    plot_feature_importance(feature_importance, indices, stddev, "gradient-boosted-classifier-feature-importance-depth-" + str(_max_depth))

def run_logistic_regression(data):
    (feature_train, feature_test, label_train, label_test) = train_test_split(data[:, 0:-1], data[:, -1].astype(int),
                                                                              test_size=0.25)

    # TODO: Type of penalty, C(Important)
    lrc = LogisticRegression(penalty='l2', dual=False, tol=0.01, C=1.0)
    lrc.fit(feature_train, label_train)
    training_error = lrc.score(feature_train, label_train)
    cross_validation_score = cross_val_score(lrc, feature_train, label_train, cv=10)
    testing_error = lrc.score(feature_test, label_test)

    print "Logistic Regression Results:"
    print "Training Accuracy:", training_error
    print "10-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)" % (cross_validation_score.mean(), cross_validation_score.std() * 2)
    print "Testing Accuracy:", testing_error

def run_all_classifiers(data):
    print "------------------------------------------"
    print "Running Random Forest..."
    run_random_forest(data, None)
    run_random_forest(data, 5)
    print "------------------------------------------"

    print "------------------------------------------"
    print "Running Gradient Boosting Classifier..."
    run_gradient_boosting_classifier(data, None)
    run_gradient_boosting_classifier(data, 5)
    print "------------------------------------------"

    print "------------------------------------------"
    print "Running Logistic Regression..."
    run_logistic_regression(data)
    print "------------------------------------------"

def test_code():
    # TEST CODE using alcoholism Data set
    alcoholism_data = get_data('alcoholism.csv', '\t')
    print "Loaded alcoholism Data, Dimensions: ", alcoholism_data.shape
    run_all_classifiers(alcoholism_data)

def main():
    # data = get_data(FILENAME, ',')
    # print "Loaded Data, Dimensions: ", data.shape
    #
    # # Disregard the first two columns(source_id, destination_id). Last column - Label
    # # TODO: Should we also disregard the third column? Personalized Pagerank Score
    # run_all_classifiers(data[:,2:])

    test_code()

if __name__ == "__main__":
    main()