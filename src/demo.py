## Run the simulation of Queue Bandits with Bernoulli (M/B/c) and Exponential (M/M/c) service rates
## Written by Debabrota Basu
from simulate_QBandits import *
from draw_the_image import *
from write_to_npy import *
import time

if __name__=='__main__':

	'''Problem setup
	u: Number f queues
	K: number of servers
	mu: True service rate matrix (u * K numpy array)
        l: True arrival rates (numpy array of size u)
	'''

        u = 1 #or 3 
	K = 5         
        # For Figure 1 of the paper
	mu = np.matrix([[0.5,0.33,0.33,0.33,0.25]])
        l = [0.3]
        # For Figure 2 of the paper
	#mu = np.matrix([[0.5,0.33,0.33,0.33,0.25],[0.33,0.5,0.25,0.33,0.25],[0.25,0.33,0.5,0.25,0.25]]) #u * K service rate matrix 
	#l = [0.3,0.25,0.2] # list of arrival rates

	'''Experimental parameters'''
	T = 10000 #time steps per simulation
	num_sim = 50 #number of simulations
        cores = 8  #number of cores in the processor


        '''Available policies are Explore, ThS, QThS, QUCB, BelMan and QBelMan'''
        policy = "QThS"

	'''Availabl service distributions are Bernoulli and Exponential'''
	service = "Bernoulli" #"Exponential" #"Bernoulli" 
        # Do not try Exponential now. There are potential bugs.
 
	'''Execute the QBandit algorithms
	 q: queue length of the bandit policy
         q0: queue length of the optimal matching
         q - q0: queue regret of the bandit policy
         sq: 2*std. deviation of q-regret
        '''
        t = time.time() # Start the clock
        (q, q0, sq) = simulate_qbandit(service, mu, u, K, l, T, policy, num_sim, cores) 
        print "Elapsed: %s" % (time.time() - t) #Stop the clock
        
	'''Write the queue regret to files and plot in an imagefile'''
        write_to_npy(u, K, q, q0, sq, policy, service)
        draw_the_image(u, K, q - q0, sq, T, policy, service)
