#Save the outputs into files
import numpy as np

def write_to_npy(u, K, x, x0, sq, policy, service):
	filename = "../results/qreg_"+str(u)+"_"+str(K)+"_"+policy+"_"+service+".npy"
	np.save(filename, x) #saving regret for all the u queues in u*t dimensional arrays
	filename = "../results/q0_"+str(u)+"_"+str(K)+"_"+policy+"_"+service+".npy"
        np.save(filename, x0) #saving regret for all the u queues in u*t dimensional arrays
	filename = "../results/sd_qreg_"+str(u)+"_"+str(K)+"_"+policy+"_"+service+".npy"
	np.save(filename, sq) #saving std. for all the u queues in u*t dimensional arrays
