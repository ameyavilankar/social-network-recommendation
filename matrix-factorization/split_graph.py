import numpy as np
import random
from sklearn.cross_validation import train_test_split

IN_FILE = "../data/facebook-combined.data"
TRAIN_FILE = "data.train"
VALIDATION_FILE = "data.validate"
PREDICT_FILE = "data.predict"
PERCENTAGE_SPLIT = 0.8

# Read the data from the file into np array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data

def save_to_file(data, filename):
    f = open(filename,'w')
    for row in data:
        f.write(str(row[0]) + " " + str(row[1]) + ", 1\n")
    f.close()

def save_predict_to_file(data, filename):
    f = open(filename,'w')
    for row in data:
        f.write(str(row[0]) + " " + str(row[1]) + "\n")
    f.close()

if __name__ == "__main__":
    # Load the Data
    data = get_data(IN_FILE, ",")
    print data.shape

    train_file = open(TRAIN_FILE,'w')
    validation_file = open(VALIDATION_FILE, 'w')

    feature_train, feature_test, label_train, label_test = train_test_split(data, np.zeros(data.shape[0]), test_size=0.2)
    
    feature_train =feature_train.astype(int)
    feature_test = feature_test.astype(int)
    # np.savetxt(TRAIN_FILE, feature_train, delimiter=',')
    # np.savetxt(VALIDATION_FILE, feature_test, delimiter=',')

    save_to_file(feature_train, TRAIN_FILE)
    save_to_file(feature_test, VALIDATION_FILE)
    save_predict_to_file(feature_test, PREDICT_FILE)

    print "Total:", data.shape
    print "Train Count", feature_train.shape
    print "Validation Count", feature_test.shape