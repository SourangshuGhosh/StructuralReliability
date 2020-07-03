#!/usr/bin/python
#import scipy._lib.messagestream
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import (QApplication,QMainWindow,QTabWidget,QDoubleSpinBox,QSpinBox, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton,QLabel,QComboBox,QRadioButton, QVBoxLayout,QHBoxLayout, QWidget,QProgressBar,QTableView,QTableWidgetItem)
from PyQt5.QtCore import QFile
from Sustained import Sustained
from Periodic import Periodic
from randomized import Randomized
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import random
import seaborn as sns
import numpy as np
import numpy
from load_utils import *
from constants import *
import pickle

class Load_tab(QtWidgets.QWidget):
    """docstring for Load_tab"""
    procStart = QtCore.pyqtSignal(numpy.ndarray)
    def __init__(self):
        super(Load_tab, self).__init__()
        self.load_tab_scrollable()
        self.plot_empty()

    def load_tab_scrollable(self):
        self.load=np.zeros(num_data_points)
        self.load_data= dict()
        self.load_data['table'] = list()
        self.load_data['load'] = list()
        self.fileName = ""
        self.fname = ""
        self.load_type = QComboBox()
        self.load_type.addItem("Sustained")
        self.load_type.addItem("Periodic")
        self.load_type.addItem("Randomized Pulse")
        self.view_load_wizard=QPushButton("Select")
        self.view_load_wizard.clicked.connect(self.view_load_generator)

        self.load_type_box = QHBoxLayout()
        self.load_type_box.addWidget(self.load_type)
        self.load_type_box.addWidget(self.view_load_wizard)

   
        self.load_generate_button=QPushButton("Add")
        self.load_clear_button=QPushButton("Clear All")
        self.load_clear_selected_button=QPushButton("Delete Selected")
        self.load_export_button = QPushButton("Export Load")
        self.load_import_button = QPushButton("Import Load")
        self.load_export_button.clicked.connect(self.writeToFile)
        self.load_import_button.clicked.connect(self.loadFromFile)

        self.load_clear_button.clicked.connect(self.plot_empty)
        self.load_generate_button.clicked.connect(self.gen_load) 
        self.load_clear_selected_button.clicked.connect(self.deleteLoadCase)       
        self.vbox=QVBoxLayout()
        self.hbox= QHBoxLayout()
        self.view_table = QTableView(self)

        self.header = self.view_table.horizontalHeader()
        self.pdata = []
        self.model = PandasModel(self.pdata)
        self.view_table.setModel(self.model)
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.view_table.update()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.resize(300,500)
        self.view_table.setFixedWidth(720)

        self.hbox.addWidget(self.view_table)
        self.hbox.addWidget(self.canvas)
    

        self.load_add_clear_box = QHBoxLayout()
    

        self.ScrollVbox= QVBoxLayout()
        
        #self.Sustained_box=Sustained()
        #self.Periodic_box = Periodic()
        #self.Randomized_box = Randomized()
        self.load_box = QGroupBox()
        self.load_box.setFixedHeight(400)

        #ScrollVbox.addWidget(self.Periodic_box)
        #ScrollVbox.addWidget(self.Randomized_box)
        self.ScrollVbox.addLayout(self.hbox)
        self.ScrollVbox.addLayout(self.load_type_box)
        #self.load_add_clear_box.addWidget(self.load_generate_button)
        self.load_add_clear_box.addWidget(self.load_clear_selected_button)
        self.load_add_clear_box.addWidget(self.load_clear_button)
        self.load_add_clear_box.addWidget(self.load_export_button)
        self.load_add_clear_box.addWidget(self.load_import_button)
        
        self.ScrollVbox.addWidget(self.load_box)
        self.ScrollVbox.addLayout(self.load_add_clear_box)
        self.setLayout(self.ScrollVbox)

    def view_load_generator(self):
        self.ScrollVbox.removeWidget(self.load_box)
        self.ScrollVbox.removeWidget(self.load_generate_button)

        self.load_box.hide()
        value= self.load_type.currentText()
        if value == "Sustained":
            self.load_box = Sustained()
        elif value == "Periodic":
            self.load_box = Periodic()
        elif value == "Randomized Pulse":
            self.load_box = Randomized()
        else:
            return

        self.ScrollVbox.addWidget(self.load_box)
        self.ScrollVbox.addWidget(self.load_generate_button)

       
    def gen_load(self):
        self.generate_load_data()
        self.update_load()
        self.plot()

    def deleteLoadCase(self):
        index_list = []                                                          
        for model_index in self.view_table.selectionModel().selectedRows():       
            index = QtCore.QPersistentModelIndex(model_index)         
            index_list.append(index.row())


        self.load_data['table'] = [i for j, i in enumerate(self.load_data['table']) if j not in index_list]
        self.load_data['load'] = [i for j, i in enumerate(self.load_data['load']) if j not in index_list]         
        #indices = self.view_table.selectionModel().selectedRows()

        self.update_load()
        if len(self.load_data['load']) != 0:
            self.plot()
            

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        # plot data
        #ax.plot(self.load)
        t_year = np.linspace(0, 1, num_data_points)
        ax.plot(t_year,self.load, label = "Final Load")
        
        self.canvas.draw()

    def plot_empty(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        # plot data
        #ax.plot(self.load)
        t_year = np.linspace(0, 1, num_data_points)
        self.load= np.zeros(num_data_points)
        self.load_data['table'] = list()
        self.load_data['load'] = list()
        ax.plot(t_year,self.load,label="Final Load" )
        self.pdata=[]
        self.model = PandasModel(self.pdata)
        self.view_table.setModel(self.model)
        self.view_table.update()

        # refresh canvas
        self.canvas.draw()

    def get_final_load(self,x):
        if len(x)==1:
            return x[0]
        return np.sum(np.array(x),axis=0)

    def generate_load_data(self):
        this_load =self.load_box.load #self.Periodic_box.load + self.Randomized_box.load + self.Sustained_box.load
        #self.pdata
        data= self.load_box.get_load_row()
        data.remove(data[1])
        self.load_data['table'].append(data[0:10])
        self.load_data['load'].append(this_load)

    
    @QtCore.pyqtSlot()
    def update_load(self):
        #self.generate_load_data()
        if len(self.load_data['load']) == 0:
            self.plot_empty()
        else:
            self.pdata = self.load_data['table']
            self.load = self.get_final_load(self.load_data['load'])
        self.model = PandasModel(self.pdata)
        self.view_table.setModel(self.model)
        self.view_table.update()
        #self.plot()
        #print(self.load_data)
        self.procStart.emit(self.load)

    def loadFromFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Load File",
               (QtCore.QDir.homePath()), "pkl (*.pkl)")
 
        if fileName:
            #print(fileName)
            with open(fileName,'rb') as f:
                data=pickle.load(f)

        if len(data['load'])!=0:     
            self.load_data= data
            #print(self.load_data)
            self.update_load()
            self.plot()
        else:
            QtWidgets.QMessageBox.about(self, "No Load", "No load found in the file")
            return
   
 
    def writeToFile(self):

        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", 
                       (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),"pkl Files (*.pkl)")
        if fileName:
           #print(fileName)
           with open(fileName,'wb') as f:
               pickle.dump(self.load_data,f)
       
 



