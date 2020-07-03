from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

from constants import *
from scipy.special import gamma
from scipy.optimize import newton
data_size= num_minutes_in_year//sampling_rate

class sampler():
    def __init__(self,dist,mean,sigma):
        self.dist=dist
        self.mean = mean
        self.sigma = sigma

    def sample(self,size=1):
        return self.get_dist_from_params(self.mean,self.sigma,self.dist)

    def get_lognormal_params(self,mean,std):
        m = mean 
        v = std
        phi = np.sqrt(v + m**2)
        mu    = np.log(m**2/phi)
        sigma = np.sqrt(np.log(phi**2/m**2))
        return mu,sigma
    
    def get_weibull_params(self,mean,std):
        mu=mean
        sig2= std*std
        f = lambda k : sig2/mu**2-gamma(1+2./k) /gamma(1+1/k)**2+1
        k0 = 1               
        k = newton(f,k0)       
        lam = mu/gamma(1+1/k)
        return k,lam

    def get_gumbel_params(self,mean,std):
        beta = np.sqrt(std*std*6/(np.pi*np.pi))
        mu= mean- 0.57721*beta
        return mu,beta

    def get_uniform_params(self,mean,std):
        b_minus_a= std/np.sqrt(12)
        bplusa = mean*2
        b = 0.5*(b_minus_a+bplusa) 
        a = 0.5*(b_minus_a-bplusa)
        return a,b

    def get_dist_from_params(self,mean,std,dist= NORMAL_DISTRIBUTION):
        if dist == NORMAL_DISTRIBUTION :
            return np.random.normal(loc=mean, scale = std)
        elif dist == UNIFORM_DISTRIBUTION :
            a,b= self.get_uniform_params(mean,std)
            return np.random.uniform(a,b)
        elif dist == LOGNORMAL_DISTRIBUTION :
            mu,sigma= self.get_lognormal_params(mean,std)
            return np.random.lognormal(mean= mu, sigma = sigma)
        elif dist == EXPONENTIAL_DISRIBUTION :
            return np.random.exponential(scale=mean)
        elif dist == WEIBULL_DISTRIBUTION :
            a,n= self.get_weibull_params(mean,std)
            return np.random.weibull(a)*n
        elif dist == GUMBEL_DISTRIBUTION :
            mu,beta= self.get_gumbel_params(mean,std)
            return np.random.gumbel(mu,beta)


class GaussianProcessEfficient():
    def __init__(self,mean,std,psd="exponential",envelope="",w_low=1,w_high=10):
        self.mean = mean
        self.std= std
        self.Wlist= np.linspace(0,20,50)
        self.psd_type= psd
        self.envelope_type= envelope
        self.w_low = w_low
        self.w_high = w_high

    def get_psd_from_type(self):
        if self.psd_type == "exponential":
            return self.psd_exponential
        elif self.psd_type == "square":
            return self.psd_square
        else:
            return self.psd_triangular

    def get_envelope_from_type(self):
        if self.envelope_type == "exponential":
            return self.envelope_exponential
        elif self.envelope_type == "sine":
            return lambda x: np.abs(np.sin(x))
        else:
            return lambda x:1

    def envelope_exponential(self,x,a=0.001):
        return np.exp(-1*x*a)

    def psd_square(self,w):
        low=self.w_low
        high=self.w_high
        strength = self.std*self.std/(high-low)
        if w >=low and w<= high:
            return strength
        else:
            return 0

    def psd_triangular(self,w):
        low=self.w_low
        high=self.w_high
        strength= 2*self.std**2/(high-low)
        if w<=low or w>=high :
            return 0
        else:
            return (w-low)*strength/(high-low)

    def psd_exponential(self,w):
        low=self.w_low
        decayRate=self.w_high
        strength= self.std**2*decayRate
        if w<=low :
            return 0
        else:
            return np.exp(-1*decayRate*(w-low))*strength

    def point(self,Wk,t,deltaW=0.25):
        phi = np.random.uniform(low=0,high=2*np.pi)
        psd= self.get_psd_from_type()
        return np.sqrt(2*abs(psd(Wk))*deltaW) * np.cos(Wk*t+phi)

    def process_at_t(self,t):
        sum=0
        for i in range(len(self.Wlist)):
            sum+=self.point(self.Wlist[i],t)
        return sum

    def process(self,time=4000):
        time_samples = np.linspace(0,time,num=time)
        process= list()
        for i in range(len(time_samples)):
            process.append(self.process_at_t(time_samples[i]))

        process=np.array(process)


        env = self.get_envelope_from_type()
        process*= env(time_samples)
        #process*= self.std
        process+= self.mean
        plt.plot(time_samples,process)
        return process


class Gaussian_process_fast:
    def __init__(self,mean,std):
        self.mean=mean
        self.std=std
        self.var=std*std
    # Define the kernel function
    def kernel(self,a, b, param):
        sqdist = np.sum(a**2,1).reshape(-1,1) + np.sum(b**2,1) - 2*np.dot(a, b.T)
        return np.exp(-.5 * (1/param) * sqdist)

    def sample(self,n=1000):
        Xtest = np.linspace(0, 1000, n).reshape(-1,1)
        self.Xtest=Xtest
        param = self.var
        K_ss = self.kernel(Xtest, Xtest, param)

        # Get cholesky decomposition (square root) of the
        # covariance matrix
        L = np.linalg.cholesky(K_ss + 1e-5*np.eye(n))
        # Sample 3 sets of standard normals for our test points,
        # multiply them by the square root of the covariance matrix
        f_prior = np.dot(L, np.random.normal(scale=self.std,size=(n)))
        #f_prior*=self.std
        f_prior+=self.mean

        return f_prior


    def sample_with_envelope(self,n=1000,env=np.sin):
        Xtest=np.linspace(0, 1000, n).reshape(-1,1)
        self.Xtest = Xtest
        param = self.var
        K_ss = self.kernel(Xtest, Xtest, param)

        # Get cholesky decomposition (square root) of the
        # covariance matrix
        L = np.linalg.cholesky(K_ss + 1e-5*np.eye(n))
        # Sample 3 sets of standard normals for our test points,
        # multiply them by the square root of the covariance matrix
        f_prior = np.dot(L, np.random.normal(scale=self.std,size=(n)))
        #f_prior*=self.std
		   
        f_prior*=env(Xtest[:,0])
        f_prior+=self.mean
        return f_prior
        #f_prior*=env(Xtest)



class StationaryLoad():
    def __init__(self,mu,sigma,load_duration=num_minutes_in_year,kernelFx="rbf",w_low=1,w_high=10):
        self.mu=mu
        self.sigma=sigma
        self.kernelFx=kernelFx
        self.load_duration= load_duration
        self.process = GaussianProcessEfficient(self.mu, self.sigma,self.kernelFx,"",w_low,w_high)

    def get_signal(self,sampling_rate=sampling_rate):
        data_points = self.load_duration//sampling_rate
        signal = self.process.process(data_points)
        return signal



class NonStaionaryLoad():
    def __init__(self,mu,sigma,load_duration=num_minutes_in_year,kernelFx='exponential',envelopFx= "",w_low=1,w_high=10):
        self.mu=mu
        self.sigma=sigma
        self.kernelFx=kernelFx
        self.envelopFx = envelopFx
        self.load_duration = load_duration
        self.process = GaussianProcessEfficient(self.mu, self.sigma,self.kernelFx,self.envelopFx,w_low,w_high)

    def get_signal(self,sampling_rate=sampling_rate):
        data_points = self.load_duration//sampling_rate
        signal = self.process.process(data_points)
        return signal


class TriangularPulse():
    def __init__(self,mu,sigma,load_duration=num_minutes_in_year,dist="Normal",width = 40):
        self.mu=mu
        self.sigma=sigma
        self.load_duration = load_duration
        self.width = width
        self.dist= dist

    def get_signal(self,sampling_rate=sampling_rate):
        data_points = self.load_duration//sampling_rate
        num_data_point=int(data_points)
        distribution = sampler(self.dist,self.mu,self.sigma)
        height= distribution.sample()
        t = np.linspace(0, 1, num_data_point)
    

        #t_year = np.linspace(0, 1, num_minutes_in_year)
        data_point=t*height#signal.sawtooth(1 * np.pi * (self.width) * t,width=0.5)*height
        #plt.plot(t_year,triangular)
        return data_point




#____________________MISC___________________________

data_points=3153
    
def gausspulse(mean,std,start,end):
    #t = np.linspace(-10, 10, 2 * 100, endpoint=False)
    gausspulse= np.zeros((data_points))
    num_data_points=int(data_points*(end-start))
    start_zeros=np.zeros((int(data_points*start)))
    t = np.linspace(-1, 1, num_data_points)
    #t_year = np.linspace(-1, 1, num_minutes_in_year)
    i, q, e = signal.gausspulse(t, fc=2, retquad=True, retenv=True)
    i*=std
    i+=mean
    final=np.append(start_zeros,i)
    trailing_zeros=np.zeros(np.shape(gausspulse)[0]-np.shape(final)[0])
    final2=np.append(final,trailing_zeros)
    gausspulse+=final2
    #plt.plot(t_year,gausspulse)
    return gausspulse
    

def square (mean,std,start,end):
    square= np.zeros((data_points))
    num_data_points=int(data_points*(end-start))
    start_zeros=np.zeros((int(data_points*start)))
    t = np.linspace(0, 1, num_data_points)
    #t_year = np.linspace(0, 1, num_minutes_in_year)
    data_points=signal.square(2 * np.pi * 5 * t)
    data_points*=std
    data_points+=mean
    final=np.append(start_zeros,data_points)
    trailing_zeros=np.zeros(np.shape(square)[0]-np.shape(final)[0])
    final2=np.append(final,trailing_zeros)
    square+=final2
    #plt.plot(t_year,square)
    return square