import numpy as np
import random
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn.metrics import roc_auc_score

# IN_FILE = "facebook.1_of_1"
IN_FILE = "output.txt"

# Read the data from the file into np array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data

if __name__ == "__main__":
    # Load the Data
    data = get_data(IN_FILE, ",")
    print "Data:", data

    if data[0][2] < 0.0:
        print ""
    y_true = np.ones(data.shape[0]).astype(int)
    y_scores = data[:, 2]

    print y_scores
    print y_true

    error = 0
    error_half = 0
    total = 0
    for row in data:
        # print row[2], 0.5
        total += 1
        if row[2] < 0:
            error += 1
        if row[2] < 0.5:
            error_half += 1

    print "Total:", total
    print "Error:", float(error)/data.shape[0]
    print "Half Error:", float(error)/data.shape[0]

    negative_indices = y_scores < 0.0
    positive_indices = y_scores > 1.0

    print "Less than zero:", negative_indices.shape
    print "Greater than one:", positive_indices.shape

    y_scores[negative_indices] = 0.0
    y_scores[positive_indices] = 1.0

    y_scores = np.append(y_scores, 0)
    y_true = np.append(y_true, 0)

    print y_true.shape, y_scores.shape
    auc_score = roc_auc_score(y_true, y_scores)

    print "AUC Score:", auc_score