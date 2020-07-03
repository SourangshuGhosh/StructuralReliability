from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import (QApplication,QMainWindow,QTabWidget,QDoubleSpinBox,QSpinBox, QCheckBox, QGridLayout, QGroupBox,QLineEdit,
        QMenu, QPushButton,QLabel,QComboBox,QRadioButton, QVBoxLayout,QHBoxLayout, QWidget,QProgressBar,QTableWidget,QTableWidgetItem)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import random
import seaborn as sns
import numpy as np
from load_utils import randomizedPoisson
from constants import *

class Randomized(QGroupBox):
    def __init__(self):
        super(Randomized, self).__init__("Randomized")
        self.initUI()
        self.plot_empty()

    def initUI(self):
        Hbox=QHBoxLayout()
        load_buttons=QGridLayout()
        load_name_label = QLabel("Name")
        self.load_name_input = QLineEdit("Randomized")
        load_type_label=QLabel("Pulse Type")
        self.load_type=QComboBox()
        self.load_type.addItem("triangular")

        load_mean_label=QLabel("Mean (in KN)")
        self.load_mean_input=QSpinBox()
        self.load_mean_input.setRange(0,300)
        self.load_mean_input.setValue(150)

        load_std_label=QLabel("Std (in KN)")
        self.load_std_input=QSpinBox()
        self.load_std_input.setRange(0,150)
        self.load_std_input.setValue(40)

        self.m_dist_type_label = QLabel("Type of Distribution")
        self.m_dist = QComboBox()
        self.m_dist.addItem("Normal")
        self.m_dist.addItem("Uniform")
        self.m_dist.addItem("Lognormal")
        self.m_dist.addItem("Exponential")
        self.m_dist.addItem("Gumbel")
        self.m_dist.addItem("Weibull")
        self.load_generate_button=QPushButton("Generate")

        load_duration_label=QLabel("Duration (in minutes)")
        self.load_duration_input=QSpinBox()
        self.load_duration_input.setRange(0,1000)
        self.load_duration_input.setValue(400)

        load_time_period_label=QLabel("Rate(Inv lambda ,in days)")
        self.load_time_period_input=QSpinBox()
        self.load_time_period_input.setRange(0,365)
        self.load_time_period_input.setValue(7)

        self.load_generate_button=QPushButton("Generate and Preview")
        self.load_generate_button.clicked.connect(self.generate_load)
        load_buttons.addWidget(load_name_label,1,1)
        load_buttons.addWidget(self.load_name_input,1,2)
        load_buttons.addWidget(load_type_label,2,1)
        load_buttons.addWidget(self.load_type,2,2)
        load_buttons.addWidget(load_mean_label,3,1)
        load_buttons.addWidget(self.load_mean_input,3,2)
        load_buttons.addWidget(load_std_label,4,1)
        load_buttons.addWidget(self.load_std_input,4,2)
        load_buttons.addWidget(self.m_dist_type_label,5,1)
        load_buttons.addWidget(self.m_dist,5,2)
        load_buttons.addWidget(load_duration_label,6,1)
        load_buttons.addWidget(self.load_duration_input,6,2)
        load_buttons.addWidget(load_time_period_label,7,1)
        load_buttons.addWidget(self.load_time_period_input,7,2)

        load_buttons.addWidget(self.load_generate_button,8,1)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        Hbox.addLayout(load_buttons)
        Hbox.addWidget(self.canvas)
        self.setLayout(Hbox)


    def get_load_row(self):
        #fetch data here
        load_name = self.load_name_input.text()
        load_type=self.load_type.currentText()
        load_mean=self.load_mean_input.value()
        load_std=self.load_std_input.value()
        load_dist = self.m_dist.currentText()
        load_duration = self.load_duration_input.value()
        time_period = self.load_time_period_input.value()

        return [load_name,load_type,load_mean,load_std,load_dist,load_duration,time_period,"-","-","-","-"]

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        # plot data
        #ax.plot(self.load)
        t_year = np.linspace(0, 1, num_data_points)
        ax.plot(t_year,self.load)

        # refresh canvas
        self.canvas.draw()

    def plot_empty(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        # plot data
        #ax.plot(self.load)
        t_year = np.linspace(0, 1, num_data_points)
        self.load= np.zeros(num_data_points)
        ax.plot(t_year,self.load)

        # refresh canvas
        self.canvas.draw()


    def generate_load(self):
        data=self.get_load_row()
        load= np.zeros((num_data_points))
        load+=self.gen_load_case(data)
        self.load=load
        self.plot()
        #return load

    def gen_load_case(self,data):
        load_type= data[1]
        load= np.zeros((num_data_points))
        mean=int(data[2])
        std =  int(data[3])
        dist = data[4] 
        duration = int(data[5])
        time_period = int(data[6])*(24*60) 
        load = randomizedPoisson(load_type,mean,std,duration,time_period,dist)
        return load

