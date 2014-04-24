import numpy as np
import random
from collections import defaultdict


IN_FILE = "yelp_full.txt"
TRAIN_FILE = "yelp_full.train"
VALIDATION_FILE = "yelp_full.validate"
PERCENTAGE_SPLIT = 0.8

# Read the data from the file into np array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data


if __name__ == "__main__":
    # Load the Data
    data = get_data(IN_FILE, ",")
    data = data.astype(int)
    print "Number of Ratings:", len(data)


    userMap = {}
    businessMap = {}
    ratingCount = 0
    for row in data:
        if row[0] not in userMap:
            userMap[row[0]] = {}

        userMap[row[0]][row[1]] = row[2]

        if row[1] not in businessMap:
            businessMap[row[1]] = {}

        businessMap[row[1]][row[0]] = row[2]

        ratingCount += 1

    print "Number of Ratings in Dict:", ratingCount
    print "Number of Users:", len(userMap)
    print "Number of Business:", len(businessMap)

    train_file = open(TRAIN_FILE,'w')
    validation_file = open(VALIDATION_FILE, 'w')

    trainCount = 0
    validationCount = 0
    total = 0
    for user, business in userMap.iteritems():
        for buss, rating in business.iteritems():
            total += 1
            if random.random() < PERCENTAGE_SPLIT:
                train_file.write(str(user) + ", " + str(buss) + ", " + str(rating) + "\n")
                trainCount += 1
            else:
                validation_file.write(str(user) + ", " + str(buss) + ", " + str(rating) + "\n")
                validationCount += 1

    print "Total:", total
    print "Train Count/Total:", trainCount, "/", total
    print "Validation Count/Total", validationCount, "/", total
    print "Train Percentage:", float(trainCount)/total

    train_file.close()
    validation_file.close()