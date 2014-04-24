import numpy as np

FILENAME = "truncated_ratings.txt"

# Read the data from the file into np array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.05, beta=0.02):
    """

    :param R: a matrix to be factorized, dimension N x M
    :param P: an initial matrix of dimension N x K
    :param Q: an initial matrix of dimension M x K

    :param K: the number of latent features
    :param steps: the maximum number of steps to perform the optimisation
    :param alpha: the learning rate
    :param beta: the regularization parameter
    :return:
    """
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = np.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )

        if step % 200 == 0:
            print "Step:", step, "Error:", e

        if e < 0.001:
            break

    return P, Q.T

if __name__ == "__main__":

    data = get_data(FILENAME, ",")
    print data.shape

    num_users = np.amax(data[:, 0]) + 1
    num_business = np.amax(data[:, 1]) + 1

    print "users", num_users
    print "bussines", num_business

    R = np.zeros((int(num_users), int(num_business)))

    for row in data:
        R[int(row[0])][int(row[1])] = row[2]


    # R = [
    #      [5,3,0,1],
    #      [4,0,0,1],
    #      [1,1,0,5],
    #      [1,0,0,4],
    #      [0,1,5,4],
    #     ]
    #
    # R = np.array(R)

    N = len(R)
    M = len(R[0])
    K = 15

    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)

    nP, nQ = matrix_factorization(R, P, Q, K)

    print "P:", nP.shape
    print "Q:", nQ.shape

    new_R = np.dot(nP, nQ.T)
    print "Matrix:", new_R
    print "Matrix Old:", R

    rmse = 0.0
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            if R[i, j] > 0:
                rmse += (R[i, j] - new_R[i, j])**2

    print "RMSE:", rmse