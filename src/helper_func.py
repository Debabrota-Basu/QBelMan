import numpy as np
from numpy.random import random_sample
import random
from math import log
from scipy.special import gamma
from scipy.special import digamma

def gamma_unbound_mat(arr):
    out = np.zeros(np.shape(arr))
    for rows in range(np.shape(arr)[0]):
       for cols in range(np.shape(arr)[1]):
           if (arr[rows,cols] <= 170):
               out[rows,cols] = np.log(gamma(arr[rows,cols]))
           else:
               out[rows,cols] = np.log(gamma(170))
               for extra in range(int(arr[rows,cols]-171)):
                   out[rows,cols] -= np.log(extra+171)
    return out

def gammaln_unbound(temp):
    if (temp <= 170):
       return np.log(gamma(temp))
    else:
       out = np.log(gamma(170))
       for extra in range(int(temp-171)):
           out += np.log(extra+171)
    return out
