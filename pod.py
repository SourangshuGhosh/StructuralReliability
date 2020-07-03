from numpy import genfromtxt
from scipy import stats
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


class POD:
	"""
	implements pod by using log(a) vs ahat model
	"""

	def __init__(self, threshold=250):
		self.datafile = "D:/BTP/ndt2.csv"
		self.ath = threshold
		my_data = genfromtxt(self.datafile, delimiter=',')
		x = np.log(my_data[:, 0])
		y = my_data[:, 1]
		slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

		self.beta0 = intercept
		self.beta1 = slope
		self.sigmay = std_err

	def get_pod(self, x):
		arg = (self.ath - (self.beta0+self.beta1*np.log(x)))/self.sigmay
		prob = norm.cdf(arg)
		return 1-prob

	def get_predicted_a(self, ahat):
		return np.exp(self.beta0+self.beta1*ahat)

    def plot_pod_curve(self):
        p=np.arange(1,50)
        x=POD()
        probs=x.get_pod(p)
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1)

        line, = ax.plot(p,probs, color='blue', lw=2)

        ax.set_xscale('log')
