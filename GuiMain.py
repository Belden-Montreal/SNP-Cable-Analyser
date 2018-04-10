from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import scipy
import MW3
import VNA_addr_dialog
import TestParameters
from Communication import Communication
import matplotlib.figure
import matplotlib.backends.backend_qt5 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.pyplot import cm 

import os

import time

import random

import pylab
from skrf import Network as rf

from snpAnalyze import SNPManipulations
import os
from os.path import splitext
import time

from Sample import Sample

import numpy as np

import threading

#import thread

from Project import Project

from calWizard import CalWizard

class ExampleApp(QtWidgets.QMainWindow, MW3.Ui_MainWindow, QtWidgets.QAction, QtWidgets.QFileDialog, QtWidgets.QListView, QtWidgets.QDialog,QtCore.Qt):


    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)

        fileMenu = self.actionImport_SnP
        newProject = self.actionNew_Project

        #Initialize sample sample Table
        self.sampleTable.setColumnCount(3)
        self.sampleTable.setHorizontalHeaderLabels(["Name","Date", "Limit"])
        self.sampleTable.setSortingEnabled(True)
        self.sampleTable.setContextMenuPolicy(self.CustomContextMenu)
        self.sampleTable.customContextMenuRequested.connect(self.tableContextMenu)        
        self.selected = []

        #Initialize Tab widget for sample info 
        

        #self.sampleTable.customContextMenuRequested.connect(self.tableContextMenu)      
        #New Project
        self.Project = Project()

        #Initialize plot parameters


        self.activeParameter = "Main"

        nav = NavigationToolbar(self.graphicsView, self)
        self.verticalLayout_3.addWidget(nav)

    def importSnp(self):
        self.openFileNamesDialog()

    def newProject(self):
        self.Project = Project()
        self.sampleTable.setRowCount(0);

    def deleteSample(self):
        pass

    def setLimit(self):
        pass

    def deembed(self):
        pass

    def setActiveSample(self):
        self.plot(None, None)

        self.selected = []
        for i in self.sampleTable.selectionModel().selectedRows():
            self.selected.append(self.sampleTable.item(i.row(),0).text())
        self.Project.activeSample = self.selected
        #print self.selected
        if len(self.selected) == 1:  #Since only one sample can be displayed at a time
            self.displaySampleParams(self.selected)
        elif len(self.selected) > 1:
            self.displaySampleParams(None)

    def displaySamplesInTable(self):
        measurementCount = len(self.Project.measurements)
        self.sampleTable.setRowCount(measurementCount)
        for i in range(0, measurementCount):
            self.sampleTable.setItem(i, 0, QtWidgets.QTableWidgetItem(self.Project.measurements[i].name))
            self.sampleTable.setItem(i, 1, QtWidgets.QTableWidgetItem(self.Project.measurements[i].date))
            self.sampleTable.setItem(i, 2, QtWidgets.QTableWidgetItem(self.Project.measurements[i].limit))
        self.sampleTable.resizeColumnsToContents()
        
    
    def openFileNamesDialog(self):
        
        options = self.Options()
        options |= self.DontUseNativeDialog
        files, _ = self.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        print(files)
        self.Project.importSNP(files)
        #self.rs.one_sided = True
        #self.rs.getParameters()
        #print 1

        #print(self.rs.RL.items())
        #print self.RL.keys()
        #self.plot(self.rs.NEXT)   USE THIS !!!!!!!

        self.displaySamplesInTable()

            #plt.legend()  # To draw legend
            #plt.show()
            #self.plot([i for i in 20*np.log10(np.absolute(self.rs.RL["36"]))])
            #print(self.rs.freq)

    def plot(self, x=None, param_dict=None):
        
        self.graphicsView.figure.clear()
        #ax.set_xlim(300*(10**3), 10**9)
        #self.ax.semilogx(x, self.pitch, '.-', label=label, c=color)
        if x is not None or param_dict is not None:
            ax=self.graphicsView.figure.add_subplot(111)
            #print param_dict.keys()
            color=iter(cm.rainbow(np.linspace(0,1,len(param_dict.keys()))))
            for key in sorted(param_dict.keys()):
                c=next(color)
                #print key

                #a = scipy.signal.decimate(x, 10)
                ax.semilogx(x, param_dict[key], label=key, c = c)


                #print key

            ax.legend(loc='upper left', ncol= 1 if len(param_dict.keys()) <= 8 else 2 )
            
            #self.figure.tight_layout()

            ax.grid(which="both")
            
            ax.set_xlabel('Freq (Hz)')
            ax.set_ylabel('dB')
            
            if self.activeParameter.replace(" ", "") == "PropagationDelay":
                ax.set_ylabel('nSec')
                
                    
            #self.ax.legend()
        self.graphicsView.draw()
        
    def tableContextMenu(self, pos):
        #print self.selected

        if len(self.selected) > 0:
            #Start by getting info on the sample. (If they're all the same type or not)
                            
            menu = QtWidgets.QMenu()
            setLimit = menu.addAction("Set Limit")
            deembed = menu.addAction("Deembed")
            setPortName = menu.addAction("Rename Ports")
                        
            test_type = menu.addMenu("Set Test Type") #Set the sub menu to select the different types of matrixes
            one_sided = test_type.addAction("One Sided")
            end_end = test_type.addAction("End to End")
            one_sided.setCheckable(True)
            end_end.setCheckable(True)
            exportExcel = menu.addAction("Export To Excel")
            delete = menu.addAction("Delete")


            #get test type for samples. If theyre all one sided, all
            #end-end or all different.
            #To start get the test type of the first sample
            _one_sided = self.Project.getSampleByName(self.selected[0]).one_sided
            print(_one_sided)
            for sample in self.selected:
                if _one_sided !=  self.Project.getSampleByName(sample).one_sided:
                    _one_sided = None
                    break                

            if _one_sided == True:
                one_sided.setChecked(True)
                end_end.setChecked(False)
            elif _one_sided == False:
                one_sided.setChecked(False)
                end_end.setChecked(True)
            else:
                one_sided.setChecked(False)
                end_end.setChecked(False)

            action = menu.exec_(QtGui.QCursor.pos())


            if action == one_sided:
                for sample in self.selected:
                    self.Project.getSampleByName(sample).reCalc(one_sided = True)
                    self.Project.activeSample = self.selected
                #print self.selected
                if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                    self.displaySampleParams(self.selected)

                elif len(self.selected) > 1:
                    self.displaySampleParams(None)
            elif action == end_end:
                for sample in self.selected:
                    self.Project.getSampleByName(sample).reCalc(one_sided = False)
                
                if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                    self.displaySampleParams(self.selected)

                elif len(self.selected) > 1:
                    self.displaySampleParams(None)
                    
            elif action == exportExcel:
                print(self.selected)
                file, _ = self.getSaveFileName(self,"Export Excel Repport", "","Excel File (*.xlsx)")
                self.Project.generateExcel(file , self.selected)
        
            #self.Project.activeMeasurements = selected
            return 1
     
        menu = QtWidgets.QMenu()
        addSNP = menu.addAction("Add Sample")
        selectAll = menu.addAction("Select All")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == selectAll:
            self.sampleTable.selectAll()
        elif action == addSNP:
            self.openFileNamesDialog()

        
    def displaySampleParams(self, sample):

        currentTab =  self.activeParameter
        print(currentTab)

        if sample == None:
            self.param_tabs.clear()
            return

        self.param_tabs.clear()

        #print sample 
        self.sample = self.Project.getSampleByName(sample[0])
        #print self.sample

        #Create a tab widget containing a main tab and all the parameters

        #Start off by creating the home tab
        self.mainTab = QtWidgets.QWidget()
        self.param_tabs.addTab(self.mainTab, "Main")

        self.tab_list = []  
        self.tab_list.append(self.mainTab)
        
        for param in self.sample.parameters:
            #print param
            self.new_tab = QtWidgets.QWidget()
            self.tab_list.append(self.new_tab)
            self.param_tabs.addTab(self.new_tab, param)
            #self.param_tabs.setCurrentIndex(self.tab_index)
            
        #self.param_tabs.currentChanged['int'].connect(self.tabChange)

        for i in range(0,self.param_tabs.count()):
            if self.param_tabs.tabText(i) == currentTab:
                index = i
                break
            else:
                index = 0
        self.param_tabs.setCurrentIndex(index)

    def tabChange(self):
        self.tab_index = self.param_tabs.currentIndex()
        self.activeParameter = self.param_tabs.tabText(self.tab_index)
        print(self.activeParameter)

        #print index
        if self.tab_index >= 1:
            self.plot(self.sample.freq, getattr(self.sample, self.activeParameter.replace(" ", "")))
        else:
            self.plot(None, None)

    def connect(self):
        connected = False
        while connected is False:
            addr = Addr_Dialog().getAddr()
            if addr:
                try:
                    print("before")
                    self.comm = Communication(addr)
                    print("done")
                    connected = True
                    self.actionWho_am_I.setEnabled(True)
                    self.actionMeasure.setEnabled(True)
                    self.actionCalibrate.setEnabled(True)
                    self.actionCalibrate_2.setEnabled(True)

                    self.actionDisconnect.setEnabled(True)
                    self.actionRun.setEnabled(True)
                    self.actionConnect.setEnabled(False)

                except Exception as e:
                    print(e)
            else:
                break

    def disconnect(self):
        connected = True
        while connected is True:
            try:
                print("before")
                self.comm.close()
                print("done")
                connected = False
                self.actionWho_am_I.setEnabled(False)
                self.actionMeasure.setEnabled(False)
                self.actionCalibrate.setEnabled(False)
                self.actionCalibrate_2.setEnabled(False)

                self.actionDisconnect.setEnabled(False)
                self.actionRun.setEnabled(False)
                self.actionConnect.setEnabled(True)

            except Exception as e:
                print(e)



    def whoAmI(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(self.comm.whoAmI())
        msg.setWindowTitle("VNA Info")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setFixedSize(msg.sizeHint())
        msg.exec_()

        
    def aquire(self):
            testName, numPorts, IF, start_freq, stop_freq, num_points, average, timeout = Test_Params_Dialog().getParams()
            if testName:
                try:
                    #comm = Communication(addr)
                    self.comm.IF = IF
                    self.comm.min_freq = start_freq
                    self.comm.max_freq = stop_freq
                    self.comm.num_points = num_points
                    self.comm.average = average

                    self.comm.aquire(testName, numPorts)
                    print(r"Y:/{}.s{}p".format(testName, numPorts))
                    self.Project.importSNP([r"Y:/{}.s{}p".format(testName, numPorts)])
                    self.displaySamplesInTable()
                except Exception as e:
                    pass

    
    def reject(self):
        pass

    def calibrate(self):
        print("CALC")
        self.comm.calibrate()
        
class Addr_Dialog:
    def getAddr(self):
        dialog = QtWidgets.QDialog()
        addr_dialog = VNA_addr_dialog.Ui_Addr_Dialog()
        addr_dialog.setupUi(dialog)
        result = dialog.exec_()
        print("here")
        if not result:
            return 0
        if result:
            addr =  addr_dialog.plainTextEdit.toPlainText()
            print("sent")
            if len(addr) < 1:
                return 0
            return addr

class Test_Params_Dialog:
    def getParams(self):
        dialog = QtWidgets.QDialog()
        params_dialog = TestParameters.Ui_TestParameterDialog()
        params_dialog.setupUi(dialog)
        result = dialog.exec_()

        if not result:
            return 0
        if result:
            try:
                testName = params_dialog.testNameLineEdit_2.text()
                IF = int(float(params_dialog.iFBandwidthLineEdit.text()))
                start_freq = int(float(params_dialog.startFrequencyLineEdit.text()))
                stop_freq = int(float(params_dialog.stopFrequencyLineEdit.text()))
                num_points = int(float(params_dialog.numberOfPointsLineEdit.text()))
                num_ports = int(float(params_dialog.numberOfPortsLineEdit.text()))
                average = int(float(params_dialog.numberOfAverageLineEdit.text()))
                timeout = int(float(params_dialog.timeoutLineEdit.text()))

                return testName, num_ports, IF, start_freq, stop_freq, num_points, average, timeout
            except Exception as e:
                print(e)



def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    app.setStyle('fusion')
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    form = ExampleApp()  # We set the  form to be our ExampleApp (design)
    form.show()  # Show the form
    sys._excepthook = sys.excepthook 
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1) 
    sys.excepthook = exception_hook 
    sys.exit(app.exec_())

    
if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function


