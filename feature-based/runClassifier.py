import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

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

def run_gradient_boosting_classifier(data, _max_depth):
    (feature_train, feature_test, label_train, label_test) = train_test_split(data[:, 0:-1], data[:, -1].astype(int),
                                                                              test_size=0.25)
    # TODO: Vary Number of Estimators and Learning Rate
    gbc = GradientBoostingClassifier(learning_rate=0.1, n_estimators=300, max_depth=_max_depth)
    gbc.fit(feature_train, label_train)
    training_error = gbc.score(feature_train, label_train)
    cross_validation_score = cross_val_score(gbc, feature_train, label_train, cv=10)
    testing_error = gbc.score(feature_test, label_test)
    # out_of_bag_improvement = gbc.oob_improvement_

    print "Random Forest Results for Max Depth:", _max_depth
    print "Training Accuracy:", training_error
    print "10-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)" % (cross_validation_score.mean(), cross_validation_score.std() * 2)
    print "Testing Accuracy:", testing_error
    # print "Out of Bag Improvement:", out_of_bag_improvement

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
    run_gradient_boosting_classifier(data, 3)
    run_gradient_boosting_classifier(data, 6)
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
    data = get_data(FILENAME, ',')
    print "Loaded Data, Dimensions: ", data.shape

    # Disregard the first two columns(source_id, destination_id). Last column - Label
    # TODO: Should we also disregard the third column? Personalized Pagerank Score
    run_all_classifiers(data[:,2:])

    # test_code()

if __name__ == "__main__":
    main()