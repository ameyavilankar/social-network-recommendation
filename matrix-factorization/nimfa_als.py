# Import nimfa library entry point for factorization
import nimfa
import numpy as np
import scipy.sparse as sparse
from scipy import array

def run_factorization(data):
    fctr = nimfa.mf(data, seed = "random_c", rank = 15, method = "snmf", max_iter = 50, initialize_only = True, version = 'r', eta = 1., beta = 1e-4, i_conv = 10, w_min_change = 0)
    fctr_res = nimfa.mf_run(fctr)

    np.set_printoptions(precision=3)
    np.set_printoptions(suppress=True)

    # Basis matrix. It is sparse, as input data was sparse as well.
    W = fctr_res.basis()
    # print "Basis matrix"
    # print W.todense()
    # print W.shape

    # Mixture matrix. We print this tiny matrix in dense format.
    H = fctr_res.coef()
    # print "Coef"
    # print H.todense()
    # print H.shape

    # Return the loss function according to Kullback-Leibler divergence. By default Euclidean metric is used.
    print "Distance Kullback-Leibler: %5.3e" % fctr_res.distance(metric = "kl")
    # Compute generic set of measures to evaluate the quality of the factorization
    sm = fctr_res.summary()
    # Print sparseness (Hoyer, 2004) of basis and mixture matrix
    print "Sparseness Basis: %5.3f  Mixture: %5.3f" % (sm['sparseness'][0], sm['sparseness'][1])
    # Print actual number of iterations performed
    print "Iterations: %d" % sm['n_iter']


    # Print estimate of target matrix data
    data_fact = np.dot(W.todense(), H.todense() )

    rmse = 0.0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i][j] > 0:
                print data[i,j], data_fact[i, j]
                rmse += (data[i, j] - data_fact[i, j])**2

    print "RMSE:", rmse
    print data, data_fact

if __name__ == "__main__":
    data = np.asarray([[0, 1, 0, 3, 0], [1, 0, 2, 1, 0], [0, 2, 0, 0, 4], [3, 1, 0, 0, 4], [0, 0, 4, 4, 0]])

    data_sparse = sparse.csr_matrix(data)

    # Print this tiny matrix in dense format
    print "Data", data_sparse.todense()
    run_factorization(data_sparse)
