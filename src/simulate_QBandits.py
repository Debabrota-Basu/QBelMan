from multiprocessing import Pool
import numpy as np
from QBandits_Ber import *
#from QBandits_Exp import *

def simulate_qbandit(service, mu, u, K, l, t, policy, num_sim, nthread):
	'''Run in parallel
	   num_sim: number of experiments
	   nthread: number of parallel threads (recommended to number of cores in the machine)
	   mu: True service rate matrix (u * K numpy array : all elements less than 1.0)
	   u: number of queues
	   K: number of servers
	   l: arrival rates (numpy array of size u)
	 '''
 	pool = Pool(processes=nthread)
	if service == "Bernoulli":
 		result = pool.map(qbandit_bernoulli, [(mu, u, K, l, t, policy)]*num_sim)
	elif service == "Exponential":
		result = pool.map(qbandit_exp, [(mu, u, K, l, t, policy)]*num_sim)
	
 	cleaned = [x for x in result if not x is None] # getting results
 	#cleaned = asarray(cleaned)
 	pool.close() # not optimal! but easy
 	pool.join()
 	(Q,Q_o) = cleaned[0]
 	Q = Q.astype(float)
 	Q_o = Q_o.astype(float)
 	vQ = np.square(Q - Q_o)
 	for i in range(1,len(cleaned)):
 		(x,y) = cleaned[i]
 		Q = Q + x.astype(float)
 		Q_o = Q_o+y.astype(float)
 		vQ = vQ + np.square(x.astype(float)-y.astype(float))
 		

 	Q = Q/num_sim
 	Q_o = Q_o/num_sim
 	vQ = vQ/(num_sim - 1)
 	sQ = abs(vQ - np.square(Q - Q_o))
 	sQ = np.sqrt(sQ)
 	return (Q,Q_o,sQ)
