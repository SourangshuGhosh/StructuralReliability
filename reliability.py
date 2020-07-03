import numpy as np

from collections import deque, defaultdict

import pywt
from numpy import fft
#from scipy.integrate import odeint

def ft(x):
    """Return simple Fourier transform surrogates.

    Returns phase randomized (FT) surrogates that preserve the power
    spectrum (or equivalently the linear correlations), but completely
    destroy the probability distribution.

    Parameters
    ----------
    x : array
        Real input array containg the time series.

    Returns
    -------
    y : array
        Surrogates with the same power spectrum as x.
    """
    y = np.fft.rfft(x)

    phi = 2 * np.pi * np.random.random(len(y))

    phi[0] = 0.0
    if len(x) % 2 == 0:
        phi[-1] = 0.0

    y = y * np.exp(1j * phi)
    return np.fft.irfft(y, n=len(x))


def aaft(x):
    """Return amplitude adjusted Fourier transform surrogates.

    Returns phase randomized, amplitude adjusted (AAFT) surrogates with
    crudely the same power spectrum and distribution as the original
    data (Theiler et al. 1992).  AAFT surrogates are used in testing
    the null hypothesis that the input series is correlated Gaussian
    noise transformed by a monotonic time-independent measuring
    function.

    Parameters
    ----------
    x : array
        1-D input array containg the time series.

    Returns
    -------
    y : array
        Surrogate series with (crudely) the same power spectrum and
        distribution.
    """
    # Generate uncorrelated Gaussian random numbers.
    y = np.random.normal(size=len(x))

    # Introduce correlations in the random numbers by rank ordering.
    y = np.sort(y)[np.argsort(np.argsort(x))]
    y = ft(y)

    return np.sort(x)[np.argsort(np.argsort(y))]



## Iaaft algorithm which preseves power spectrum as well as amlitude distirbution 

def iaaft(x, maxiter=1000, atol=1e-8, rtol=1e-10):
    """Return iterative amplitude adjusted Fourier transform surrogates.

    Returns phase randomized, amplitude adjusted (IAAFT) surrogates with
    the same power spectrum (to a very high accuracy) and distribution
    as the original data using an iterative scheme (Schreiber & Schmitz
    1996).

    Parameters
    ----------
    x : array
        1-D real input array of length N containing the time series.
    maxiter : int, optional (default = 1000)
        Maximum iterations to be performed while checking for
        convergence.  The scheme may converge before this number as
        well (see Notes).
    atol : float, optional (default = 1e-8)
        Absolute tolerance for checking convergence (see Notes).
    rtol : float, optional (default = 1e-10)
        Relative tolerance for checking convergence (see Notes).

    Returns
    -------
    y : array
        Surrogate series with (almost) the same power spectrum and
        distribution.
    i : int
        Number of iterations that have been performed.
    e : float
        Root-mean-square deviation (RMSD) between the absolute squares
        of the Fourier amplitudes of the surrogate series and that of
        the original series.

    Notes
    -----
    To check if the power spectrum has converged, we see if the absolute
    difference between the current (cerr) and previous (perr) RMSDs is
    within the limits set by the tolerance levels, i.e., if abs(cerr -
    perr) <= atol + rtol*perr.  This follows the convention used in
    the NumPy function numpy.allclose().

    Additionally, atol and rtol can be both set to zero in which
    case the iterations end only when the RMSD stops changing or when
    maxiter is reached.
    """
    # Calculate "true" Fourier amplitudes and sort the series.
    ampl = np.abs(np.fft.rfft(x))
    sort = np.sort(x)

    # Previous and current error.
    perr, cerr = (-1, 1)

    # Start with a random permutation.
    t = np.fft.rfft(np.random.permutation(x))

    for i in range(maxiter):
        # Match power spectrum.
        s = np.real(np.fft.irfft(ampl * t /( np.abs(t)+1e-10), n=len(x)))

        # Match distribution by rank ordering.
        y = sort[np.argsort(np.argsort(s))]

        t = np.fft.rfft(y)
        cerr = np.sqrt(np.mean((ampl ** 2 - np.abs(t) ** 2) ** 2))

        # Check convergence.
        if abs(cerr - perr) <= atol + rtol * abs(perr):
            break
        else:
            perr = cerr

    # Normalize error w.r.t. mean of the "true" power spectrum.
    return y, i, cerr / np.mean(ampl ** 2)

# this function applies iaaft on wavelet coefficients 
def coef_aaft(x):
    temp=list()
    for i in range(len(x)):
        #temp.append((iaaft(x[i][0])[0],iaaft(x[i][1])[0]))
        temp.append((aaft(x[i][0]),aaft(x[i][1])))
        #temp[i][1]=iaaft(x[i][1])[0]
        
    return temp

def coef_iaaft(x):
    temp=list()
    for i in range(len(x)):
        temp.append((iaaft(x[i][0])[0],iaaft(x[i][1])[0]))
        #temp.append((aaft(x[i][0]),aaft(x[i][1])))
        #temp[i][1]=iaaft(x[i][1])[0]
        
    return temp

# returns as surrogate series from the original series
def gen_surrogates(x,method="Wavelet"):
    if method=='Wavelet2' :
        z=pywt.swt(x,wavelet='haar')
        rand=coef_iaaft(z)
        series=pywt.iswt(rand,wavelet='haar')
        return series
    elif method== 'Wavelet':
        z=pywt.swt(x,wavelet='haar')
        rand=coef_aaft(z)
        series=pywt.iswt(rand,wavelet='haar')
        return series
    elif method=='FT':
        series=ft(x)
        return series
    elif method== 'AAFT':
        series=aaft(x)
        return series
    elif method == 'IAAFT':
        series=iaaft(x)
        return series
        
        
        
        

def reversals(series):
    """
    A generator function which iterates over the reversals in the iterable
    *series*. Reversals are the points at which the first
    derivative on the series changes sign. The generator never yields
    the first and the last points in the series.
    """
    series = iter(series)
    
    x_last, x = next(series), next(series)
    d_last = (x - x_last)
    
    for x_next in series:
        if x_next == x:
            continue
        d_next = x_next - x
        if d_last * d_next < 0:
            yield x
        x_last, x = x, x_next
        d_last = d_next



def extract_cycles(series):
    """
    Returns two lists: the first one containig full cycles and the second
    containing one-half cycles. The cycles are extracted from the iterable
    *series* according to section 5.4.4 in ASTM E1049 (2011).
    """
    points = deque()
    full, half = [], []

    for x in reversals(series):
        points.append(x)
        while len(points) >= 3:
            # Form ranges X and Y from the three most recent points
            X = abs(points[-2] - points[-1])
            Y = abs(points[-3] - points[-2])

            if X < Y:
                # Read the next point
                break
            elif len(points) == 3:
                # Y contains the starting point
                # Count Y as one-half cycle and discard the first point
                half.append(Y)
                points.popleft()
            else:
                # Count Y as one cycle and discard the peak and the valley of Y
                full.append(Y)
                last = points.pop()
                points.pop()
                points.pop()
                points.append(last)
    else:
        # Count the remaining ranges as one-half cycles
        while len(points) > 1:
            half.append(abs(points[-2] - points[-1]))
            points.pop()
    return full, half



def count_cycles(series, ndigits=None):
    """
    Returns a sorted list containig pairs of cycle magnitude and count.
    One-half cycles are counted as 0.5, so the returned counts may not be
    whole numbers. The cycles are extracted from the iterable *series*
    using the extract_cycles function. If *ndigits* is given the cycles
    will be rounded to the given number of digits before counting.
    """
    full, half = extract_cycles(series)
    
    # Round the cycles if requested
    if ndigits is not None:
        full = (round(x, ndigits) for x in full)
        half = (round(x, ndigits) for x in half)
    
    # Count cycles
    counts = defaultdict(float)
    for x in full:
        counts[x] += 1.0
    for x in half:
        counts[x] += 0.5
    
    return (counts.items())


#______________________RAINFLOW ENDS______________________




##_____delta a calculation function __________

def deltaA(deltaP,x,c,m):
    #Virkler sample
    W=152.4
    B=2.54
    L=558.8
    noise=np.random.normal(0,0.1,size=(int(deltaP[1]+1),1))
    noise=np.power(10,noise)
    noise=np.mean(noise)
    corr=np.sqrt(1/np.cos(3.141592*x/(W)))
    return 10**c*deltaP[1]*(((deltaP[0]/(B*W/1000))*np.sqrt(3.141492*x/1000)*corr)**m)*noise


def make_simulations(N,method="Wavelet"):
    load=3*np.random.randn(10000)+3
    final=list()
    for i in range(N):
        surr=gen_surrogates(load,method)
        
        ##parameters of paris law
        mu_m= 2.881456950623539
        mu_c=-7.051804738743373
        sig_m =0.16133993007844813
        
        sig_c=0.16738100437155728
        
        rho=-0.9882044
        ## sample a0 from a given initial distribution
        a0=np.random.normal(9,1, 1)[0]
    
        mean=[mu_m,mu_c]
        cov1=rho*sig_m*sig_c
        cov=[[sig_m**2, cov1],[cov1,sig_c**2]]
        
        m, c = np.random.multivariate_normal(mean, cov, 1).T
        cycles=list(count_cycles(surr,ndigits=2))
        af=a0
        for j in range(len(cycles)):
            af=af+deltaA(cycles[j],af,c,m)
            
        final.append(af[0])
    return final
    
