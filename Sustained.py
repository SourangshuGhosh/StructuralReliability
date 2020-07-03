from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import (QApplication,QMainWindow,QTabWidget,QDoubleSpinBox,QSpinBox, QCheckBox, QGridLayout, QGroupBox,QLineEdit,
        QMenu, QPushButton,QLabel,QComboBox,QRadioButton, QVBoxLayout,QHBoxLayout, QWidget,QProgressBar,QTableWidget,QTableWidgetItem)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import random
import seaborn as sns
import numpy as np
from load_utils import sustained
from constants import *

class Sustained(QGroupBox):
    def __init__(self):
        super(Sustained, self).__init__("Sustained")
        self.initUI()
        self.plot_empty()

    def initUI(self):
        Hbox=QHBoxLayout()
        load_buttons=QGridLayout()
        load_name_label = QLabel("Name")
        self.load_name_input = QLineEdit("Sustained")
        load_type_label=QLabel("Load Type")
        self.load_type=QComboBox()
        self.load_type.addItem("stationary")
        self.load_type.addItem("non-stationary")
        #self.load_type.addItem("triangular")
        self.acf_label = QLabel("Spectrum Type")
        self.psd = QComboBox()
        self.psd.addItem("Square")
        self.psd.addItem("Triangular")
        self.psd.addItem("Exponential")

        psd_param_label=QLabel("Spectrum Params a and b (range [a,b] or a*e^-bw )")
        self.psd_param1_input=QSpinBox()
        self.psd_param1_input.setRange(0,50)
        self.psd_param1_input.setValue(1)
        #self.psd_param1_input.setPlaceholderText("a") 
        self.psd_param2_input=QSpinBox()
        self.psd_param2_input.setRange(0,50)
        self.psd_param2_input.setValue(10)
        self.psd_param_box = QHBoxLayout()
        self.psd_param_box.addWidget(self.psd_param1_input)
        self.psd_param_box.addWidget(self.psd_param2_input)

        self.envelope_label = QLabel("Envelope F(x)")
        self.envelope = QComboBox()
        self.envelope.addItem("sine")
        self.envelope.addItem("exponential")
               
        load_mean_label=QLabel("Mean (in KN)")
        self.load_mean_input=QSpinBox()
        self.load_mean_input.setRange(0,300)
        self.load_mean_input.setValue(150)
        load_std_label=QLabel("Std (in KN)")
        self.load_std_input=QSpinBox()
        self.load_std_input.setRange(0,150)
        self.load_std_input.setValue(40)
        # self.m_dist_type_label = QLabel("Type of Distribution")
        # self.m_dist = QComboBox()
        # self.m_dist.addItem(NORMAL_DISTRIBUTION)
        # self.m_dist.addItem(UNIFORM_DISTRIBUTION)
        # self.m_dist.addItem(LOGNORMAL_DISTRIBUTION)
        # self.m_dist.addItem(EXPONENTIAL_DISRIBUTION)
        # self.m_dist.addItem(GUMBEL_DISTRIBUTION)
        # self.m_dist.addItem(WEIBULL_DISTRIBUTION)
        self.load_generate_button=QPushButton("Generate and Preview")
        self.load_generate_button.clicked.connect(self.generate_load)
        load_buttons.addWidget(load_name_label,1,1)
        load_buttons.addWidget(self.load_name_input,1,2)
        load_buttons.addWidget(load_type_label,2,1)
        load_buttons.addWidget(self.load_type,2,2)
        load_buttons.addWidget(self.acf_label,3,1)
        load_buttons.addWidget(self.psd,3,2)
        load_buttons.addWidget(psd_param_label,4,1)
        load_buttons.addLayout(self.psd_param_box,4,2)
        load_buttons.addWidget(self.envelope_label,5,1)
        load_buttons.addWidget(self.envelope,5,2)
        load_buttons.addWidget(load_mean_label,6,1)
        load_buttons.addWidget(self.load_mean_input,6,2)
        load_buttons.addWidget(load_std_label,7,1)
        load_buttons.addWidget(self.load_std_input,7,2)
        
        #load_buttons.addWidget(self.m_dist_type_label,8,1)
        #load_buttons.addWidget(self.m_dist,8,2)
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
        load_psd = self.psd.currentText()
        load_envelope = self.envelope.currentText()
        #load_dist = self.m_dist.currentText()
        load_mean=self.load_mean_input.value()
        load_std=self.load_std_input.value()
        w_low = self.psd_param1_input.value()
        w_high = self.psd_param2_input.value()

        if load_type == "stationary":
            load_envelope="-"

        return [load_name,load_type,load_mean,load_std,"-","-","-",load_psd,load_envelope,w_low,w_high]

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
        mean=int(data[2])
        std =  int(data[3]) 
        dist = data[4]
        acf = data[7]
        envelope= data[8]
        w_low = float(data[9])
        w_high = float(data[10])
        load = sustained(load_type,mean,std,acf,envelope,dist,w_low,w_high)
        return load

