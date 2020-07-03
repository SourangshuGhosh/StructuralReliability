#!/usr/bin/python
#import scipy._lib.messagestream
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
from reliability import *
from constants import *
import time
import sip
import sys
from load_tab import Load_tab
from home_tab import Home_tab
from bayesian_tab import Bayesian_tab

class AppContext(QMainWindow):
  def __init__(self):
    # Initialize tab screen
    super(AppContext, self).__init__()
    result=QWidget()
    layout=QVBoxLayout()
    tabs = QTabWidget()
    #tab1 = self.home_tab_ui() 
    self.tab1=Home_tab()
    #tab2 = self.load_tab_ui()
    self.tab2=Load_tab()
    #tab3=self.bayesian_tab_ui()
    self.tab3=Bayesian_tab()
    self.tab4=self.about_tab_ui()

    self.tab2.procStart.connect(self.tab1.load_generated)
    tabs.addTab(self.tab1,"Home")
    tabs.addTab(self.tab2,"Load")
    tabs.addTab(self.tab3,"Bayesian Updatation")
    tabs.addTab(self.tab4,"About")
    layout.addWidget(tabs)
    result.setLayout(layout)

    result.setWindowTitle("Reliability-IITKGP")
    result.resize(1024,720)
    self.setCentralWidget(result)
    self.setWindowTitle("Reliability-IITKGP")
    self.showMaximized()
    

    #return result
  
  def bayesian_tab_ui(self):
    self.bayesian=QtWidgets.QWidget()
    coming_soon_lab=QLabel("Coming Soon")
    vbox=QVBoxLayout()
    vbox.addWidget(coming_soon_lab)
    self.bayesian.setLayout(vbox)
    return self.bayesian

  def about_tab_ui(self):
    self.about=QtWidgets.QWidget()
    coming_soon_lab=QLabel("Coming Soon")
    vbox=QVBoxLayout()
    vbox.addWidget(coming_soon_lab)
    self.about.setLayout(vbox)
    return self.about


def main():
   app = QApplication(sys.argv)
   ex = AppContext()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()