# Import nimfa library entry point for factorization
import nimfa
import numpy as np

# Construct sparse matrix in CSR format, which will be our input for factorization
from scipy.sparse import csr_matrix
from scipy import array
from numpy import dot
V = np.asarray([[0, 1, 0, 3, 0], [1, 0, 2, 1, 0], [0, 2, 0, 0, 4], [3, 1, 0, 0, 4], [0, 0, 4, 4, 0]])

# Print this tiny matrix in dense format
# print V.todense()
print V.shape, V


fctr = nimfa.mf(V, seed = "random_c", rank = 10, method = "snmf", max_iter = 12, initialize_only = True, version = 'r', eta = 1., beta = 1e-4, i_conv = 10, w_min_change = 0)
fctr_res = nimfa.mf_run(fctr)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

# Basis matrix. It is sparse, as input V was sparse as well.
W = fctr_res.basis()
print "Basis matrix"
# print W.todense()
print W.shape, W

# Mixture matrix. We print this tiny matrix in dense format.
H = fctr_res.coef()
print "Coef"
# print H.todense()
print H.shape, H

# Return the loss function according to Kullback-Leibler divergence. By default Euclidean metric is used.
print "Distance Kullback-Leibler: %5.3e" % fctr_res.distance(metric = "kl")

# Compute generic set of measures to evaluate the quality of the factorization
sm = fctr_res.summary()
# Print sparseness (Hoyer, 2004) of basis and mixture matrix
print "Sparseness Basis: %5.3f  Mixture: %5.3f" % (sm['sparseness'][0], sm['sparseness'][1])
# Print actual number of iterations performed
print "Iterations: %d" % sm['n_iter']


# Print estimate of target matrix V
print "Estimate"
print np.dot(W, H)