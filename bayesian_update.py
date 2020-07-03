import numpy as np
from scipy.stats import norm
import scipy.integrate as integrate
import matplotlib.pyplot as plt

ameas=[1.175, 1.125]

lb=0.9
ub=1.3
ath=0.3


def bayesian_update(ahat,lb,ub,ath):
	#TODO: get these from POD class
	mu_hat=0.05502402; # parameters from regression analysis
	sigma_hat=0.00710946#
	sigma=0.1 
	Nsamp=100
	ameas=list()
	ameas.append(ahat)
	prior = lambda a0 :1/(ub-lb)

	ntrials=Nsamp
	s=len(ameas)
	L= lambda a0: 1
	l=1

	for i in range(len(ameas)):
	    POD= lambda a0 : norm.cdf(a0,loc=mu_hat,scale=sigma_hat)
	            
	    if ameas[i] <= ath:
	        L1= lambda a0 : (1-POD(a0))/(ath-0)
	    else:
	        L1= lambda a0 : POD(a0)*norm.pdf(a0,loc=ameas[i],scale=sigma)
	    
	    L2= lambda a0 : L(a0)*L1(a0)
	    #L=L2

	D = lambda a0 :L2(a0)*prior(a0)
	I=integrate.quad(D,0,10)

	f_update = lambda a0 : L2(a0)*prior(a0)/I[0]
	return f_update

	# x= np.linspace(lb,ub+2,50)
	# y=[f_update(x) for x in x]
	# plt.plot(x,y)
	# plt.plot([lb,lb,ub,ub],[0,1/(ub-lb),1/(ub-lb),0],"--")