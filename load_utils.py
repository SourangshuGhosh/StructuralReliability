from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import random
from PyQt5 import QtWidgets,QtGui,QtCore
from load_types import StationaryLoad,NonStaionaryLoad,TriangularPulse

from constants import num_minutes_in_year,num_data_points,sampling_rate


def load_signal_factory(type,mu,sigma,duration = num_minutes_in_year,psd="exponential",envelope="exponential",w_low=1,w_high=10):
    if type == "stationary":
        return StationaryLoad(mu,sigma,duration,psd,w_low,w_high)
    elif type == "non-stationary":
        return NonStaionaryLoad(mu,sigma,duration,psd,envelope,w_low,w_high)
    elif type == "triangular":
        return TriangularPulse(mu,sigma,duration)


def sustained(load_type,mu,sigma,kernelFx="exponential",envelopeFx="",dist = "Normal",w_low=1,w_high=10):
    load_signal=load_signal_factory(load_type,mu,sigma,num_minutes_in_year,kernelFx,envelopeFx,w_low,w_high)
    load_data = load_signal.get_signal()
    return load_data

def periodic(load_type,mu,sigma,duration,time_period,dist= "Normal",psd="exponential",envelope="exponential",w_low=1,w_high=10):
    load_signal = load_signal_factory(load_type,mu,sigma,duration,psd,envelope,w_low,w_high)
    single_signal= load_signal.get_signal()
    zeros_to_append = (int(time_period)//sampling_rate) - len(single_signal)
    zeros= np.zeros(zeros_to_append)
    single_signal = np.append(single_signal,zeros)
    req_rep = (num_data_points//len(single_signal)) +1
    load_data = np.tile(single_signal,req_rep)
    load_data = load_data[0:num_data_points]
    return load_data
    

def randomizedPoisson(load_type,mu,sigma,duration,rate,dist="Normal"):
    load_len=0
    while load_len<num_data_points :
        time_period = random.expovariate(1/rate)
        zeros_to_append = int(time_period)//sampling_rate
        load_signal = load_signal_factory(load_type,mu,sigma,duration)
        single_signal= load_signal.get_signal()
        zeros= np.zeros(zeros_to_append)
        signal_next = np.append(zeros,single_signal)
        if load_len == 0:
            signal = signal_next
        else:
            signal = np.append(signal,signal_next)
        
        load_len = len(signal)  
    load_data = signal[0:num_data_points]
    return load_data

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    x=ret[n - 1:] / n
    y=np.append(x,x[0:n-1])
    return y


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = np.array(data)
        self._cols = ["Name","Mean","Std","Distribution","Duration","Time Period","Spectrum","Envelope","a","b"]
        if data:
            self.r, self.c = np.shape(self._data)
        else:
            self.r,self.c =0,0

    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return '%s' % self._data[index.row(),index.column()]
        return None


    def headerData(self, p_int, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._cols[p_int]
            elif orientation == QtCore.Qt.Vertical:
                return p_int
        return None