import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import time


class ALSMatrixFactorization():
    def __init__(self, counts, num_factors=40, num_iterations=30,
                 reg_param=0.02):
        self.counts = counts
        self.num_users = counts.shape[0]
        self.num_items = counts.shape[1]
        self.num_factors = num_factors
        self.num_iterations = num_iterations
        self.reg_param = reg_param

    def train_model(self):
        self.user_vectors = np.random.normal(size=(self.num_users,
                                                   self.num_factors))
        self.item_vectors = np.random.normal(size=(self.num_items,
                                                   self.num_factors))

        for i in xrange(self.num_iterations):
            t0 = time.time()
            print 'Solving for user vectors...'
            self.user_vectors = self.iteration(True, sparse.csr_matrix(self.item_vectors))
            print 'Solving for item vectors...'
            self.item_vectors = self.iteration(False, sparse.csr_matrix(self.user_vectors))
            t1 = time.time()
            print 'iteration %i finished in %f seconds' % (i + 1, t1 - t0)

        return (self.user_vectors, self.item_vectors)

    def iteration(self, user, fixed_vecs):
        num_solve = self.num_users if user else self.num_items
        num_fixed = fixed_vecs.shape[0]
        YTY = fixed_vecs.T.dot(fixed_vecs)
        eye = sparse.eye(num_fixed)
        lambda_eye = self.reg_param * sparse.eye(self.num_factors)
        solve_vecs = np.zeros((num_solve, self.num_factors))

        t = time.time()
        for i in xrange(num_solve):
            if user:
                counts_i = self.counts[i].toarray()
            else:
                counts_i = self.counts[:, i].T.toarray()
            CuI = sparse.diags(counts_i, [0])
            pu = counts_i.copy()
            pu[np.where(pu != 0)] = 1.0
            YTCuIY = fixed_vecs.T.dot(CuI).dot(fixed_vecs)
            YTCupu = fixed_vecs.T.dot(CuI + eye).dot(sparse.csr_matrix(pu).T)
            xu = spsolve(YTY + YTCuIY + lambda_eye, YTCupu)
            solve_vecs[i] = xu
            if i % 1000 == 0:
                print 'Solved %i vecs in %d seconds' % (i, time.time() - t)
                t = time.time()

        return solve_vecs


# Read the data from the file into np array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data


if __name__ == "__main__":
    # FILENAME = "truncated_ratings.txt"
    # data = get_data(FILENAME, ",")
    # print data.shape
    #
    # num_users = np.amax(data[:, 0]) + 1
    # num_business = np.amax(data[:, 1]) + 1
    #
    # print "users", num_users
    # print "bussines", num_business
    #
    # R = np.zeros((int(num_users), int(num_business)))
    #
    # for row in data:
    #     R[int(row[0])][int(row[1])] = row[2]

    R = [
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ]
    R = np.array(R)
    R_sparse = sparse.csr_matrix(R)

    als_fact = ALSMatrixFactorization(R_sparse)

    nP, nQ = als_fact.train_model()

    print "P:", nP.shape
    print "Q:", nQ.shape

    new_R = np.dot(nP, nQ.T)
    print "Matrix:", new_R
    print "Matrix Old:", R

    rmse = 0.0
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            if R[i, j] > 0:
                rmse += (R[i, j] - new_R[i, j]) ** 2

    print "RMSE:", rmse