#!/usr/bin/python
# import scipy._lib.messagestream
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QDoubleSpinBox, QSpinBox, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QLabel, QComboBox, QRadioButton, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar, QTableWidget, QTableWidgetItem)

from PyQt5.QtCore import QRect

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import seaborn as sns
import numpy as np
import numpy
from reliability import *
from constants import *
from load_types import sampler


class Home_tab(QtWidgets.QWidget):
    """docstring for Home_tab"""

    def __init__(self):
        super(Home_tab, self).__init__()
        self.load_tab()
        self.load = np.zeros(num_seconds_in_year)

    def load_tab(self):
        self.result = QtWidgets.QWidget()
        self.v_box = QtWidgets.QVBoxLayout()
        self.Paris_law_box = QGroupBox("Paris Law Parameters")
        # grid1 = QGridLayout("Paris Law Parmeters")
        self.Paris_law_hbox = QGridLayout()

        self.m_lab = QLabel("Parameters of m ")
        self.m_mean_lab = QLabel("mean")
        self.m_std_lab = QLabel("std")
        self.c_lab = QLabel("Parameters of c in mm")
        self.c_mean_lab = QLabel("mean")
        self.c_std_lab = QLabel("std")
        self.corr_lab = QLabel("correlation coeff between m and c")
        self.m_mean_input = QDoubleSpinBox()
        self.m_mean_input.setRange(-1000, 1000)
        self.m_mean_input.setValue(m_mean)
        self.c_mean_input = QDoubleSpinBox()
        self.c_mean_input.setRange(-1000, 1000)
        self.c_mean_input.setValue(c_mean)
        self.m_std_input = QDoubleSpinBox()
        self.m_std_input.setRange(0, 1000)
        self.m_std_input.setValue(m_std)
        self.c_std_input = QDoubleSpinBox()
        self.c_std_input.setRange(0, 1000)
        self.c_std_input.setValue(c_std)
        self.corr_c_m_input = QDoubleSpinBox()
        self.corr_c_m_input.setRange(-1, 1)
        self.corr_c_m_input.setValue(corr_c_m)
        self.Paris_law_hbox.addWidget(self.m_lab, 0, 0)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.m_mean_lab, 0, 1)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.m_mean_input, 0, 2)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.m_std_lab, 0, 3)
        self.Paris_law_hbox.addWidget(self.m_std_input, 0, 4)

        self.m_dist_type_label = QLabel("Type of Distribution")
        self.m_dist = QComboBox()
        self.m_dist.setGeometry(QRect(40, 40, 491, 31))
        self.m_dist.setObjectName("Distribution")
        self.m_dist.addItem(NORMAL_DISTRIBUTION)
        #self.m_dist.addItem(UNIFORM_DISTRIBUTION)
        #self.m_dist.addItem(LOGNORMAL_DISTRIBUTION)
        #self.m_dist.addItem(EXPONENTIAL_DISRIBUTION)
        #self.m_dist.addItem(GUMBEL_DISTRIBUTION)
        #self.m_dist.addItem(WEIBULL_DISTRIBUTION)
        self.Paris_law_hbox.addWidget(self.m_dist_type_label, 0, 5)
        self.Paris_law_hbox.addWidget(self.m_dist, 0, 6)

        self.Paris_law_hbox.addWidget(self.c_lab, 1, 0)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.c_mean_lab, 1, 1)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.c_mean_input, 1, 2)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.c_std_lab, 1, 3)
        self.Paris_law_hbox.addWidget(self.c_std_input, 1, 4)

        self.c_dist_type_label = QLabel("Type of Distribution")
        self.c_dist = QComboBox()
        self.c_dist.setGeometry(QRect(40, 40, 491, 31))
        self.c_dist.setObjectName("Distribution")
        self.c_dist.addItem(NORMAL_DISTRIBUTION)
        #self.c_dist.addItem(UNIFORM_DISTRIBUTION)
        #self.c_dist.addItem(LOGNORMAL_DISTRIBUTION)
        #self.c_dist.addItem(EXPONENTIAL_DISRIBUTION)
        #self.c_dist.addItem(GUMBEL_DISTRIBUTION)
        #self.c_dist.addItem(WEIBULL_DISTRIBUTION)
        self.Paris_law_hbox.addWidget(self.c_dist_type_label, 1, 5)

        self.Paris_law_hbox.addWidget(self.c_dist, 1, 6)
        self.Paris_law_hbox.addWidget(self.corr_lab, 2, 2)
        # Paris_law_hbox.addStretch()
        self.Paris_law_hbox.addWidget(self.corr_c_m_input, 2, 3)
        self.Paris_law_box.setLayout(self.Paris_law_hbox)

        self.intial_dist_box = QGroupBox("Inital Distribution Parameters")
        # grid1 = QGridLayout("Paris Law Parmeters")
        self.intial_dist_hbox = QGridLayout()
        self.init_mean_lab = QLabel("Mean")
        self.init_std_lab = QLabel("Std Deviation")
        self.init_mean_input = QDoubleSpinBox()
        self.init_mean_input.setRange(0, 1000)
        self.init_mean_input.setValue(10)
        self.init_std_input = QDoubleSpinBox()
        self.init_std_input.setRange(0, 100)
        self.init_std_input.setValue(2)

        self.intial_dist_hbox.addWidget(self.init_mean_lab, 0, 0)
        # Paris_law_hbox.addStretch()
        self.intial_dist_hbox.addWidget(self.init_mean_input, 0, 1)
        # Paris_law_hbox.addStretch()
        self.intial_dist_hbox.addWidget(self.init_std_lab, 0, 2)
        # Paris_law_hbox.addStretch()
        self.intial_dist_hbox.addWidget(self.init_std_input, 0, 3)
        # Paris_law_hbox.addStretch()

        self.init_dist_type_label = QLabel("Type of Distribution")
        self.init_dist = QComboBox()
        self.init_dist.setGeometry(QRect(40, 40, 491, 31))
        self.init_dist.setObjectName("Distribution")
        self.init_dist.addItem(NORMAL_DISTRIBUTION)
        self.init_dist.addItem(UNIFORM_DISTRIBUTION)
        self.init_dist.addItem(LOGNORMAL_DISTRIBUTION)
        self.init_dist.addItem(EXPONENTIAL_DISRIBUTION)
        self.init_dist.addItem(GUMBEL_DISTRIBUTION)
        self.init_dist.addItem(WEIBULL_DISTRIBUTION)
        self.intial_dist_hbox.addWidget(self.init_dist_type_label, 1, 0)

        self.intial_dist_hbox.addWidget(self.init_dist, 1, 1)
        self.intial_dist_box.setLayout(self.intial_dist_hbox)

        # Monte Carlo parameters Box
        self.monte_carlo_box = QGroupBox("Monte Carlo Parameters")
        self.monte_carlo_hbox = QHBoxLayout()
        self.num_iterations_lab = QLabel("Number of iterations")
        self.num_iterations_input = QSpinBox()
        self.num_iterations_input.setRange(0, 100000000)
        self.num_iterations_input.setValue(num_iterations)
        self.monte_carlo_hbox.addWidget(self.num_iterations_lab)
        self.monte_carlo_hbox.addStretch()
        self.monte_carlo_hbox.addWidget(self.num_iterations_input)
        self.monte_carlo_hbox.addStretch()
        self.monte_carlo_box.setLayout(self.monte_carlo_hbox)

        self.Surrogate_load_box = QGroupBox("Load Generation")
        self.Surrogate_load_hbox = QHBoxLayout()
        self.load_gen_method_lab = QLabel("Method for Load Generation")
        self.load_gen_method = QComboBox()
        self.load_gen_method.setGeometry(QRect(40, 40, 491, 31))
        self.load_gen_method.setObjectName("Method")
        self.load_gen_method.addItem("FT")
        self.load_gen_method.addItem("AAFT")
        self.load_gen_method.addItem("IAAFT")
        self.load_gen_method.addItem("Wavelet+AAFT")
        self.load_gen_method.addItem("Wavelet+IAAFT")

        self.Surrogate_load_hbox.addWidget(self.load_gen_method_lab)
        self.Surrogate_load_hbox.addStretch()
        self.Surrogate_load_hbox.addWidget(self.load_gen_method)
        self.Surrogate_load_hbox.addStretch()

        self.Surrogate_load_box.setLayout(self.Surrogate_load_hbox)

        self.submit_box = QGroupBox()
        self.submit_hbox = QHBoxLayout()

        self.submit = QPushButton("Submit")
        self.cancel = QPushButton("Cancel")

        self.submit.clicked.connect(self.onSubmit)
        self.cancel.clicked.connect(self.onCancel)
        # self.submit_hbox.addStretch()
        self.submit_hbox.addWidget(self.submit)
        self.submit_hbox.addStretch()
        self.submit_hbox.addWidget(self.cancel)
        self.submit_hbox.addStretch()
        self.submit_box.setLayout(self.submit_hbox)
        # add all boxes in main vbox layout
        self.v_box.addWidget(self.Paris_law_box)
        self.v_box.addStretch()
        self.v_box.addWidget(self.intial_dist_box)
        self.v_box.addStretch()
        self.v_box.addWidget(self.monte_carlo_box)
        self.v_box.addStretch()
        self.v_box.addWidget(self.Surrogate_load_box)
        self.v_box.addStretch()
        self.v_box.addWidget(self.submit_box)

        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # grid.addWidget(comboBox,2,0)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.final_cracks = list()

        self.v_box.addWidget(self.canvas)
        self.v_box.addWidget(self.progressBar)

        self.setLayout(self.v_box)
        # return self.result

    @QtCore.pyqtSlot(numpy.ndarray)
    def load_generated(self, load):
        self.load = load

    def onSubmit(self):
        self.get_values()
        if np.sum(self.load)==0:
            QtWidgets.QMessageBox.about(self, "No Load", "Please add a load from load tab")
            return
        self.myLongTask = TaskThread(
            self.final_cracks, self.handle_result, self.parameters, self.load)
        self.myLongTask.notifyProgress.connect(self.onProgress)
        self.onStart()  # start calculating

    def onCancel(self):
        self.myLongTask.terminate()
        # self.progressBar.setValue(0)

    def onStart(self):
        # self.get_values()
        # print(self.parameters)
        self.myLongTask.start()

    def onProgress(self, i):
        self.progressBar.setValue(i)

    def handle_result(self, data):
        self.final_cracks = data.val
        self.plot()

    def get_values(self):
        temp = dict()
        temp['m_mean'] = self.m_mean_input.value()
        temp['m_std'] = self.m_std_input.value()
        temp['m_dist'] = self.m_dist.currentText()
        temp['c_mean'] = self.c_mean_input.value()
        temp['c_std'] = self.c_std_input.value()
        temp['c_dist'] = self.c_dist.currentText()
        temp['corr_c_m'] = self.corr_c_m_input.value()
        temp['method'] = self.load_gen_method.currentText()
        temp['num_iterations'] = self.num_iterations_input.value()
        temp['init_mean'] = self.init_mean_input.value()
        temp['init_std'] = self.init_std_input.value()
        temp['init_dist'] = self.init_dist.currentText()
        self.parameters = temp

    def plot(self):

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        self.final_cracks= np.array(self.final_cracks)
        self.final_cracks = self.final_cracks[~np.isnan(self.final_cracks)]
        sns.distplot(self.final_cracks, axlabel= "Final Crack Size Distribution (in mm)",ax=ax)
        self.canvas.draw()


class ResultObj(QtCore.QObject):
    def __init__(self, val):
        self.val = val


class TaskThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(object)

    def __init__(self, final_cracks, callback, params, load, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.final_cracks = final_cracks
        self.finished.connect(callback)
        self.params = params
        self.load = load
        self.setTerminationEnabled()

    notifyProgress = QtCore.pyqtSignal(int)
    # def run(self):
    #   for i in range(101):
    #     self.notifyProgress.emit(i)
    #     time.sleep(0.1)

    def run(self):
        print(self.params)
        load = self.load

        #load=3*np.random.randn(10000)+3
        print(len(load))
        N = self.params['num_iterations']
        method = self.params['method']
        self.final_cracks = list()
        #m_sampler = sampler(self.params['m_dist'],self.params['m_mean'],self.params["m_std"])
        initialDistibutionSampler = sampler(self.params['init_dist'],self.params['init_mean'],self.params["init_std"])
        for i in range(N):
            surr = gen_surrogates(load, method)

            # parameters of paris law
            # mu_m= 2.881456950623539
            # mu_c=-7.051804738743373
            # sig_m =0.16133993007844813

            # sig_c=0.16738100437155728

            # rho=-0.9882044
            mu_m = self.params['m_mean']
            mu_c = self.params['c_mean']
            sig_m = self.params['m_std']
            sig_c = self.params['c_std']
            rho = self.params['corr_c_m']

            # initial distribution params
            #init_m = self.params['init_mean']
            #init_std = self.params['init_std']
            # sample a0 from a given initial distribution

            a0 = initialDistibutionSampler.sample()#np.random.normal(init_m, init_std, 1)[0]

            mean = [mu_m, mu_c]
            cov1 = rho*sig_m*sig_c
            cov = [[sig_m**2, cov1], [cov1, sig_c**2]]

            m, c = np.random.multivariate_normal(mean, cov, 1).T
            cycles = list(count_cycles(surr, ndigits=2))
            af = a0
            for j in range(len(cycles)):
                af = af+deltaA(cycles[j], af, c, m)

            self.final_cracks.append(af[0])
            self.notifyProgress.emit(((i+1)*100//N))

        self.finished.emit(ResultObj(self.final_cracks))
        print(self.final_cracks)
