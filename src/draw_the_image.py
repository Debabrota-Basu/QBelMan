## Visualize the queue regrets in plots
import numpy as np
import matplotlib.pyplot as plt

def draw_the_image(u, K, x, sq, T, policy, service):
        imagename = "../results/qreg_"+str(u)+"_"+str(K)+"_"+policy+"_"+service+".pdf"
        colors=iter(plt.cm.rainbow(np.linspace(0,1,u)))
        for count in range(u):
               name = "Queue" + str(count+1)
               color_code = next(colors)
               plt.plot(np.linspace(1,np.size(x[0:,count]),np.size(x[0:,count])), x[0:,count], c=color_code, label=name)
               plt.fill_between(np.linspace(1,np.size(x[0:,count]),np.size(x[0:,count])), np.squeeze(np.asarray(x[0:,count]-sq[0:,count]/2)),np.squeeze(np.asarray(x[0:,count]+sq[0:,count]/2)),alpha=0.2)
        plt.xlim(0,T)
        #plt.ylim(-20,20)
        plt.xlabel('Time')
        plt.ylabel('Queue regret')
        plt.legend(loc='best')
        plt.savefig(imagename,bbox_inches='tight')
	plt.show()
