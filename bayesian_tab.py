from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import (QApplication,QMainWindow,QTabWidget,QDoubleSpinBox,QSpinBox, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton,QLabel,QComboBox,QRadioButton, QVBoxLayout,QHBoxLayout, QWidget,QProgressBar,QTableWidget,QTableWidgetItem)

from PyQt5.QtCore import QSize, QRect

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import random
import seaborn as sns
import numpy as np
from bayesian_update import  bayesian_update
from constants import *

class Bayesian_tab(QtWidgets.QWidget):
    """docstring for Bayesian_tab"""
    def __init__(self):
        super(Bayesian_tab, self).__init__()
        self.load_tab()

    def load_tab(self):
        self.load=QtWidgets.QWidget()
        vbox=QVBoxLayout()
        parameters_box=QGroupBox("Parameter")
        parameters=QGridLayout()
        ahat_label=QLabel("A hat")
        self.ahat_input=QDoubleSpinBox()
        self.ahat_input.setRange(0,100)
        self.ahat_input.setValue(1.12)
        lb_label=QLabel("Lower Bound")
        self.lb_input=QDoubleSpinBox()
        self.lb_input.setRange(0,100)
        self.lb_input.setValue(0.9)
        ub_label=QLabel("Upper Bound")
        self.ub_input=QDoubleSpinBox()
        self.ub_input.setRange(0,10)
        self.ub_input.setValue(1.3)
        ath_label=QLabel("Ath")
        self.ath_input=QDoubleSpinBox()
        self.ath_input.setRange(0,10)
        self.ath_input.setValue(0.3)
        
        
        self.bayesian_update_button=QPushButton("Calculate")
        parameters.addWidget(ahat_label,1,1)
        parameters.addWidget(self.ahat_input,1,2)
        parameters.addWidget(lb_label,2,1)
        parameters.addWidget(self.lb_input,2,2)
        parameters.addWidget(ub_label,3,1)
        parameters.addWidget(self.ub_input,3,2)
        parameters.addWidget(ath_label,4,1)
        parameters.addWidget(self.ath_input,4,2)
        parameters_box.setLayout(parameters)

        vbox.addWidget(parameters_box)
        vbox.addStretch()
        vbox.addWidget(self.bayesian_update_button)
        self.bayesian_update_button.clicked.connect(self.plot)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)

    def plot(self):
        self.get_values()
        ahat=self.params['ahat']
        ub=self.params['ub']
        lb=self.params['lb']
        ath=self.params['ath']
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        f_update=bayesian_update(ahat,lb,ub,ath)
        x= np.linspace(lb,ub+2,50)
        y=[f_update(x) for x in x]
        ax.plot(x,y)
        ax.plot([lb,lb,ub,ub],[0,1/(ub-lb),1/(ub-lb),0],"--")    

        # refresh canvas
        self.canvas.draw()



    def get_values(self):
        temp=dict()
        temp['ahat']=self.ahat_input.value()
        temp['ub']=self.ub_input.value()
        temp['lb']=self.lb_input.value()
        temp['ath']=self.ath_input.value()
        self.params=temp

