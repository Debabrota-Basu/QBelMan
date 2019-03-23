from Match_Q_S import *
from helper_func import *

def one_step_schedule(P,mu,u,K,q,N,ucb_avg,l):
	'''one scheduling step
	 P : permutation matrix
	 mu : actual transmission rate
	 K : number of queues
	 q : current queuelengths
	 N : number of samplings to be updates
	 avg : number of samplings
	'''
	rates  = np.diag(P*np.transpose(mu))
        for i in range(u):
        	bit = random.random()
        	if bit <= l[i]:
            		q[i] = q[i] + 1 
    	nodes = P*np.transpose(np.matrix(range(K)))
    	for i in range(u):
        	bit = random.random()
        	if bit <= rates[i]:
            	#print "testing"
            	# updates the number of wins and losses and number of iterations
            		if q[i] != 0 :
                		q[i] = q[i] - 1
            		ucb_avg[i,int(nodes[i])] = (N[i,int(nodes[i])]*ucb_avg[i,int(nodes[i])] + 1)/(N[i,int(nodes[i])]+1)
            		N[i,int(nodes[i])] = N[i,int(nodes[i])] + 1
        	else:
            		ucb_avg[i,int(nodes[i])] = (N[i,int(nodes[i])]*ucb_avg[i,int(nodes[i])])/(N[i,int(nodes[i])]+1)
            		N[i,int(nodes[i])] = N[i,int(nodes[i])] + 1

def stat_sample(lam,mu,num,tol):
	values = range(tol)
	prob = [0]*tol
	prob[0] = 1 - lam/mu
	prob[1] = lam*(mu - lam)/((mu**2)*(1 - lam))
	s = prob[0] + prob[1]
	for i in range(2,tol):
		prob[i] = prob[1]*(lam*(1-mu)/(mu*(1 - lam)))**(i-1)
		s = s + prob[i]
	for i in range(tol) :
		prob[i] = prob[i]/s
	#print values
	#print prob
	return np.random.choice(values,size = num, p = prob)[0]#weighted_values(values,prob,num)


def qbandit_policy(mu,u,K,l,t,policy):
	np.random.seed()
	random.seed()
 	q = [0]*u
 	q_o = [0]*u
	N = np.zeros([u,K])
	ucb_avg = np.zeros([u,K])
	N_o = np.zeros([u,K])
	ucb_avg_o = np.zeros([u,K])
	for i in range(u):
		mui = np.amax(mu[i,:])
		lam = l[i]
		q[i] = stat_sample(lam,mui,1,200)
		q_o[i] = q[i]
	queue = np.empty((0,u),int)
	queue_o = np.empty((0,u),int)
	queue = np.append(queue, np.array([q]), axis=0)
	queue_o = np.append(queue_o, np.array([q_o]), axis=0)
	P_o = max_match(mu,u,K)
	P_exp = []
	for i in range(K):   #these are the explore schedules
		P = []
		for j in range(u):
			h = [0]*K
			h[(j+i)%K] = 1
			P = P + [h]
		P = np.matrix(P)
		P_exp = P_exp + [P]	
	s = 0
	for i in range(K):
		one_step_schedule(P_exp[i],mu,u,K,q,N,ucb_avg,l)
		queue = np.append(queue, np.array([q]), axis=0)
		one_step_schedule(P_o,mu,u,K,q_o,N_o,ucb_avg_o,l)
		queue_o = np.append(queue_o, np.array([q_o]), axis=0)
		s = s + 1

	while (s < t):
		bit = random.random()
                if ((policy == "ThS") or (policy == "UCB")):
                        threshold = 0.0
                elif (policy == "Explore"):
			threshold = float(t)
		else:
                        threshold = float(3*K*(log(s)**2)/s) #QUCB paper has experimented with float(3*K*(log(s)**3)/s) and float(4*K/s)
		if (bit <= threshold):
			values = range(K)
			prob = [float(1./K)]*K
			index = np.random.choice(range(K))
			one_step_schedule(P_exp[index],mu,u,K,q,N,ucb_avg,l)
			s = s + 1
			queue = np.append(queue, np.array([q]), axis=0)
		else:
			ucb_mat = np.zeros([K,K])
                        if policy == "QBelMan":
                                #Nbar,Sbar = pseudobelief(ucb_avg,N,s)
                                Nbar = np.mean(np.squeeze(np.asarray(N)))
                                Sbar = np.mean(np.squeeze(np.asarray(N))*np.squeeze(np.asarray(ucb_avg)))
			for i in range(u):
				for j in range(K):
                                        if ((policy == "QThS") or (policy == "ThS")):
                                            ucb_mat[i,j] = np.random.binomial(1,np.random.beta(ucb_avg[i,j]*N[i,j]+0.5,(1-ucb_avg[i,j])*N[i,j]+0.5)) #for QThompson
                                        elif ((policy == "QUCB") or (policy == "UCB")):
                                               ucb_mat[i,j] = ucb_avg[i,j] + ((log(s)**2)/(2*N[i,j]))**0.5 #for UCB or QUCB
					       #ucb_mat[i,j] = ucb_avg[i,j] + ((log(s)**3)/(2*N[i,j]))**0.5 
                                        elif policy == "QBelMan":
                                               ## BelMan or QBelMan
                                               itau = log(s) + 200*log(log(s))                    
                                               c2 = gammaln_unbound(N[i,j]*ucb_avg[i,j]) + gammaln_unbound(N[i,j]*(1-ucb_avg[i,j])) - gammaln_unbound(N[i,j])
                                               ucb_mat[i,j] = itau*ucb_avg[i,j] + c2 + (Sbar-N[i,j]*ucb_avg[i,j])*digamma(N[i,j]*ucb_avg[i,j]) + (Nbar-Sbar-N[i,j]*(1-ucb_avg[i,j]))*digamma(N[i,j]*(1-ucb_avg[i,j])) - (Nbar-N[i,j])*digamma(N[i,j]) 

                        P_s = max_match(ucb_mat,u,K)     #matches queues and servers with maximum weight instead of just choosing the maxima       
 			one_step_schedule(P_s,mu,u,K,q,N,ucb_avg,l) #updates the variables further
 			s = s+1
 			queue = np.append(queue, np.array([q]), axis=0)
 		if (s%1000 == 0):
                    print "Time step = %d" % s
                    #print ucb_avg
                    #print N

                #The Optimal scheduling
                one_step_schedule(P_o,mu,u,K,q_o,N_o,ucb_avg_o,l)
		queue_o = np.append(queue_o, np.array([q_o]), axis=0)
                                        
 	return queue,queue_o


def qbandit_bernoulli(sim):
	'''Helper Function '''
	return qbandit_policy(sim[0], sim[1], sim[2], sim[3], sim[4], sim[5])



