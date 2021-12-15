from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt

import sys
import scipy

from UI import MainWindow
from UI import VNA_addr_dialog
from UI import MainWidget

from dialogs import pairNameDialog
from dialogs.connectDialog import ConnectDialog
from dialogs.vna_test import VNATestDialog

from print2console import EmittingStream

from widgets.ParameterWidget import ParameterWidget
from widgets.EmbeddingWidget import EmbeddingWidget
from widgets.AlienWidget import AlienWidget
from widgets.PlugWidget import PlugWidget

from widgets.ConsoleWidget import ConsoleWidget


from limits.LimitDialog import LimitDialog

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

from settings import Settings

from snpAnalyze import SNPManipulations
import os
from os.path import splitext
import time

from Sample import Sample

import numpy as np

import threading
import multiprocessing

#import thread

from Project import Project

from calWizard import CalWizard

from decimal import Decimal


import matplotlib.ticker

from tabThread import TabThread

from multiprocessing.dummy import Pool as ThreadPool

from genericworker import GenericWorker

class BeldenSNPApp(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow, QtWidgets.QAction, QtWidgets.QFileDialog, QtWidgets.QListView, QtWidgets.QDialog, QtCore.Qt):

    '''
    This class handles all of the user sent commands from the GUI.   

    '''

    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self)

        fileMenu = self.actionImport_SnP
        newProject = self.actionNew_Project

        #Initialize sample sample Table 
        self.sampleTable.setColumnCount(4)
        self.sampleTable.setHorizontalHeaderLabels([None, "Name","Date", "Limit"])
        self.sampleTable.setSortingEnabled(True)
        self.sampleTable.setContextMenuPolicy(self.CustomContextMenu)
        self.sampleTable.customContextMenuRequested.connect(self.tableContextMenu)
        self.selected = []

        #Initialize Tab widget for sample info

        #self.sampleTable.customContextMenuRequested.connect(self.tableContextMenu)
        #New Project
        self.Project = Project()

        #Initialize plot parameters

        self.activeParameter = "Main" #We want the the first sample tab to display to be the Main tab.
                                                                            

        nav = NavigationToolbar(self.graphicsView, self)  #Sets up the menu at the bottom of the GUI which lets us interact with the matplotlib plots
        self.verticalLayout_3.addWidget(nav)


        #Here, we process any arguments that might be sent the program from outside of the interface.
        #In other words, when ever a user right click on an SNP files, rather than opening them in Notepad, it would be opened in this interface.
        arguments = sys.argv[1:] 
        
        if len(arguments):
            self.Project.importSNP(arguments)
            self.displaySamplesInTable()
            
        self.comm = Communication()
        self.settings = Settings()

        self.threadpool = QtCore.QThreadPool()
        self.poolMutex = QtCore.QMutex()

        self.paramWidgetList = []

        # Comment out this line to get messanges to appear in terminal instead of in app. 
        self.setupConsole()


    #@QtCore.pyqtSlot()
    def addPlug(self):   
        testName, result = QtWidgets.QInputDialog.getText(self, "Add a Plug Sample",
                                                                "Please enter a plug name")
        if result and len(testName) > 0 and not testName.isspace():
            print("%s!" % testName)
            self.Project.addPlug(testName)
            self.displaySamplesInTable()
        else:
            return

    def addEmbed(self):
        testName, result = QtWidgets.QInputDialog.getText(self, "Add an Embedded Sample",
                                                                "Please enter a sample name")
        if result and len(testName) > 0 and not testName.isspace():
            print("%s!" % testName)
            self.Project.addEmbed(testName)
            self.displaySamplesInTable()
        else:
            return
        
    def addAlien(self):
        testName, result = QtWidgets.QInputDialog.getText(self, "Add an Alien Test",
                                                                "Please enter a Test name")
        if result and len(testName) > 0 and not testName.isspace():
            print("%s!" % testName)
            self.Project.addAlien(testName)
            self.displaySamplesInTable()
        else:
            return

    def newProject(self):
        
        self.Project = Project()
        self.sampleTable.setRowCount(0)

    def deleteSample(self):
        
        self.Project.delete(self.selected)
        self.displaySamplesInTable()
        self.setActiveSample()

    def setLimit(self):
        type = None
        if self.selected[0].__repr__() == "Embed" or self.selected[0].__repr__() == "Plug" :
            type = "Embedding"
        limitDialog = LimitDialog(type = type)
        result = limitDialog.showDialog()
        if result:
            item = limitDialog.getSelection().internalPointer().standard
            for limit in item.limits.values():
                if not (limit == ""):
                    for function in limit.functions:
                        for symbol in function.free_symbols:
                            if not (str(symbol) == 'f'):
                                ret = QtWidgets.QInputDialog.getDouble(self, "Enter the parameter value", "Please enter the value for the parameter "+ str(symbol) +" : ")
                                limit.setParamValue(symbol, ret[0])
            
            for sample in self.selected:

                worker = GenericWorker(sample.setStandard , standard=item)
                worker.signals.finished.connect(self.displaySamplesInTable)

                self.threadpool.start(worker)


    def setActiveSample(self):
        self.plot(None, None)

        self.selected = []
        for i in self.sampleTable.selectionModel().selectedRows():
            self.selected.append(self.sampleTable.item(i.row(),0).data(Qt.UserRole))
        #print self.selected
        if len(self.selected) >= 1:
            self.Project.activeSample = self.selected
           
        
        if len(self.selected) == 1:  #Since only one sample can be displayed at a time

            if self.selected[0].__repr__() == "Alien":
                self.setupAlien()

            elif self.selected[0].__repr__() == "Embed":
                self.setupEmbed()

            
            elif self.selected[0].__repr__() == "Plug":
                self.setupPlug()

            elif self.selected[0].__repr__() == "SNP":
                self.displaySampleParams(self.selected)
        
        elif len(self.selected) > 1 or len(self.selected) < 1:
            self.displaySampleParams(None)

            
    def displaySamplesInTable(self):
        #self.blockSignals( False )

        print("Finished TREAD !")
        self.blockSignals(False)

        measurementCount = len(self.Project.measurements)
        self.sampleTable.setRowCount(measurementCount)
        for i, measurement in enumerate(self.Project.measurements):



            #Column 0 (type)
            type = measurement.__repr__()[0]
            self.sampleTable.setItem(i, 0, QtWidgets.QTableWidgetItem(type))
            self.sampleTable.item(i, 0).setData(Qt.UserRole, measurement)

            #Column 1 (name)
            self.sampleTable.setItem(i, 1, QtWidgets.QTableWidgetItem(measurement.name))
            self.sampleTable.item(i, 1).setData(Qt.UserRole, measurement)
            
            #Column 2 (date)
            self.sampleTable.setItem(i, 2, QtWidgets.QTableWidgetItem(measurement.date))
            self.sampleTable.item(i, 2).setData(Qt.UserRole, measurement)

            #Column 3 (standard)
            if measurement.standard is not None:
                self.sampleTable.setItem(i, 3, QtWidgets.QTableWidgetItem(measurement.standard.name))
                self.sampleTable.item(i, 3).setData(Qt.UserRole, measurement)
        
        self.sampleTable.resizeColumnsToContents()
        self.setActiveSample()

    
    def setupEmbed(self):
        self.param_tabs.clear()
        self.embeddingWidget = EmbeddingWidget(self.param_tabs,  sample = self.selected[0], graph=self.graphicsView, comm = self.comm, project=self.Project)
        self.embeddingWidget.proc_addPlug.connect(self.addPlug)

        
        #self.param_tabs.addTab(self.embeddingWidget.widget, "Embedding Main")


    def setupPlug(self):
        self.param_tabs.clear()
        self.plugWidget = PlugWidget(self.param_tabs,  sample = self.selected[0], graph=self.graphicsView, comm = self.comm)
        #self.param_tabs.addTab(self.embeddingWidget.widget, "Embedding Main")
        
    def setupAlien(self):
        self.param_tabs.clear()
        self.alienWidget = AlienWidget(self.param_tabs,  sample = self.selected[0], graph=self.graphicsView, comm = self.comm)
        #self.param_tabs.addTab(self.embeddingWidget.widget, "Embedding Main")
        

    def importSnp(self):
        #Whenever the user clicks on the import SNP button, it opens a file dialog

        options = self.Options()
        options |= self.DontUseNativeDialog
        files, _ = self.getOpenFileNames(self, "Select SNP(s)", "","sNp Files (*.s*p)", options=options)
        #print files
        print(files)

        #This needs to be in thread  Look into this : https://realpython.com/python-pyqt-qthread/

        #for file in files:
        #self.blockSignals( True )

        self.blockSignals(True)

        worker = GenericWorker(function= self.Project.importSNP, files = files)
        worker.signals.finished.connect(self.displaySamplesInTable)

        self.threadpool.start(worker)


        #self.my_worker.start.connect(self.my_worker.run)


        '''self.threadPool.append(my_thread)
        self.my_worker = my_worker


        self.importSNPTask = self.Project.importSNP(samples = files)
        self.importSNPTask.notifyFinished.connect(self.displaySamplesInTable)
        self.importSNPTask.started.connect(self.startImport)
        self.importSNPTask.start.emit()'''


        #self.Project.importSNP(files)

        #print(self.rs.RL.items())
        #self.plot(self.rs.NEXT) USE THIS !!!!!!!

        #self.displaySamplesInTable()

    def startImport(self):
        print("START IMPORT THREAD : ", int(QtCore.QThread.currentThreadId()))


    def plot(self, x=None, param_dict=None, limit = None, unit = "Mhz", avgLimit = None):

        self.graphicsView.figure.clear()
        #ax.set_xlim(300*(10**3), 10**9)
        #self.ax.semilogx(x, self.pitch, '.-', label=label, c=color)
        if x is not None or param_dict is not None:
            ax=self.graphicsView.figure.add_subplot(111)
            #print param_dict.keys()
            color=iter(cm.rainbow(np.linspace(0,1,len(param_dict.keys()))))
            for key in sorted(param_dict.keys()):
                c = next(color)
                #print key

                #a = scipy.signal.decimate(x, 10)
                if len(x) == len(param_dict[key]):
                    ax.semilogx(x, param_dict[key], label=key, c = c)
                #print key 

            ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())


            #self.figure.tight_layout()

            ax.grid(which="both")

            ax.set_xlabel('Freq ({})'.format(unit))
            ax.set_ylabel('dB')
            ax.set_title(self.activeParameter)
            if self.activeParameter.replace(" ", "") == "PropagationDelay":
                ax.set_ylabel('nSec')

            if limit is not None:
                ax.semilogx(*zip(*limit), linestyle = '--', label="limit", c = c)

            if avgLimit is not None:
                ax.semilogx(*zip(*avgLimit), linestyle = '--', label="average limit", c = c)
            ax.legend(loc='upper left', ncol = 1 if len(param_dict.keys()) <= 8 else 2 )
     
            #self.ax.legend()
        self.graphicsView.draw()


    def pairRename(self):
        pair_names = self.settings.pairNames
        num_pairs = self.settings.numPairs
        try:
            names = pairNameDialog.PairNameDialog(pair_names, num_pairs).getPairNames()
            self.settings.pairNames = names
        except Exception as e:
            print(e)

    def pairRenameAlien(self):
        pair_names = self.settings.pairNamesAlien
        num_pairs = self.settings.numPairs
        try:
            names = pairNameDialog.PairNameDialog(pair_names, num_pairs).getPairNames()
            self.settings.pairNamesAlien = names
        except Exception as e:
            print(e)


    def setPairNumberAlien(self):
        sample = self.selected[0]

        pair_names = sample.port_name
        num_pairs = sample.numPairs
        try:
            names = pairNameDialog.PairNameDialog(pair_names, num_pairs).getPairNames()
            #self.settings.pairNamesAlien = names
            sample.port_rename(names)
            if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                self.setupAlien() 

        except Exception as e:
            print(e)



    def setPairNumber(self):
        sample = self.selected[0]
        if sample.__repr__() == "Alien":
            self.setPairNumberAlien()
            return
        snp = sample.snpFile
        sided = sample.one_sided
        standard = sample.standard

        pair_names = sample.port_name

        try:

            names = pairNameDialog.PairNameDialog(pair_names, sample.num_ports_dd).getPairNames()
            #self.settings.pairNames = names


            sample.__init__(snp, sided, standard, pair_names = names)
            sample.getParameters()
            sample.setStandard(standard)
            self.Project.activeSample = self.selected
            #print self.selected
            if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                self.displaySampleParams(self.selected) 

        except Exception as e:
            print(e)

    def tableContextMenu(self, pos):
        #print self.selected
        try:
            if len(self.selected) > 0 and all("SNP" in  sample.__repr__()  for sample in self.selected):
                #Start by getting info on the sample. (If they're all the same type or not)

                menu = QtWidgets.QMenu()
                setLimit = menu.addAction("Set Limit")

                if len(self.selected) == 1: 

                    setPairNumber = menu.addAction("Renumber Pairs")

                test_type = menu.addMenu("Set Test Type") #Set the sub menu to select the different types of matrixes
                one_sided = test_type.addAction("One Sided")
                end_end = test_type.addAction("End to End")
                one_sided.setCheckable(True)
                end_end.setCheckable(True)
                exportExcel = menu.addAction("Export To Excel")
                exportPDF = menu.addAction("Export To PDF")

                delete = menu.addAction("Delete")

                #get test type for samples. If theyre all one sided, all
                #end-end or all different.
                #To start get the test type of the first sample
                _one_sided = self.selected[0].one_sided
                print(_one_sided)
                for sample in self.selected:
                    if _one_sided !=  sample.one_sided:
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
                        sample.reCalc(one_sided = True)
                        self.Project.activeSample = self.selected
                    #print self.selected
                    if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                        self.displaySampleParams(self.selected)

                    elif len(self.selected) > 1:
                        self.displaySampleParams(None)
                elif action == end_end:
                    for sample in self.selected:
                        sample.reCalc(one_sided = False)

                    if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                        self.displaySampleParams(self.selected)

                    elif len(self.selected) > 1:
                        self.displaySampleParams(None)

                elif action == exportExcel:
                    print(self.selected)
                    self.generateExcel()

                elif action == exportPDF:
                    print(self.selected)
                    self.generatePDF()

                elif action == delete:
                    self.deleteSample()

                elif action == setLimit:
                    self.setLimit()
                #self.Project.activeMeasurements = selected

                elif action == setPairNumber and len(self.selected) == 1:
                    self.setPairNumber()
                return 1


            elif len(self.selected) > 0 and not all("SNP" in  sample.__repr__()  for sample in self.selected):

                menu = QtWidgets.QMenu()
                setLimit = menu.addAction("Set Limit")

                if len(self.selected) == 1:
                    setPairNumber = menu.addAction("Renumber Pairs")

                exportExcel = menu.addAction("Export To Excel")
                exportPDF = menu.addAction("Export To PDF")

                delete = menu.addAction("Delete")

                #get test type for samples. If theyre all one sided, all
                #end-end or all different.
                #To start get the test type of the first sample

                action = menu.exec_(QtGui.QCursor.pos())

                if action == exportExcel:
                    print(self.selected)
                    self.generateExcel()

                elif action == exportPDF:
                    print(self.selected)
                    self.generatePDF()

                elif action == delete:
                    self.deleteSample()

                elif action == setLimit:
                    self.setLimit()

                elif action == setPairNumber and len(self.selected) == 1:
                    self.setPairNumber()
                #self.Project.activeMeasurements = selected
                return 1

            menu = QtWidgets.QMenu()
            addSNP = menu.addAction("Add Sample")
            addAlien = menu.addAction("Add Alien Sample")
            addEmbed = menu.addAction("Add Emdedding Sample")
            addPlug = menu.addAction("Add Plug Sample")

            selectAll = menu.addAction("Select All")
            action = menu.exec_(QtGui.QCursor.pos())
            if action == selectAll:
                self.sampleTable.selectAll()
            elif action == addSNP:
                self.importSnp()
            elif action == addAlien:
                self.addAlien()
            elif action == addEmbed:
                self.addEmbed()
            elif action == addPlug:
                self.addPlug()


        except Exception as e:
            print(e)

    def generateExcel(self):
        #file, _ = self.getSaveFileName(self,"Export Excel Repport", "","Excel File (*.xlsx)")
        if len(self.selected) == 0:
            samples = self.Project.measurements
        else:
            samples = self.selected
            print(samples)
        self.Project.generateExcelReport(samples)

    def generatePDF(self):
        #file, _ = self.getSaveFileName(self,"Export Excel Repport", "","Excel File (*.xlsx)")
        if len(self.selected) == 0:
            samples = self.Project.measurements
        else:
            samples = self.selected
        self.Project.generatePDFReport(samples)

    def displaySampleParams(self, sample):

        currentTab =  self.activeParameter

        if sample == None:
            self.param_tabs.clear()
            return
        
        self.param_tabs.clear()

        #print sample
        self.sample = sample[0]
        #print self.sample

        #Create a tab widget containing a main tab and all the parameters

        #Start off by creating the home tab
        self.mainTab = QtWidgets.QWidget()
        self.mainTabWidget = MainWidget.Ui_MainWidget()
        self.mainTabWidget.setupUi(self.mainTab)
        self.setupMainTab()
        self.param_tabs.addTab(self.mainTab, "Main")

        self.tab_list = []
        self.tab_list.append(self.mainTab)

        self.paramWidgetList = []
        self.paramWidgetList.append(None)

        #values = self.calculateErrors(pool=os.cpu_count())
        allPass = True
        failedParams = []
        self.blockSignals(True)

        for param in self.sample.parameters:

            self.new_tab = ParameterWidget(param.replace(" ", ''), self.sample , graph = self.graphicsView) #, values[param.replace(" ","")])
            self.paramWidgetList.append(self.new_tab)
            self.tab_list.append(self.new_tab.widget)
            self.param_tabs.addTab(self.new_tab.widget, param)

            allPass = allPass and self.new_tab.hasPassed
            if not self.new_tab.hasPassed:
                failedParams.append(param)

        if allPass:
            self.mainTabWidget.passLabel.setText("Pass")
        else:
            self.mainTabWidget.passLabel.setText("Fail")
        self.mainTabWidget.failsLabel.setText(str(failedParams))

        for i in range(0,self.param_tabs.count()):
            if self.param_tabs.tabText(i) == currentTab:
                index = i
                break
            else:
                index = 0
        self.blockSignals(False)

        self.param_tabs.setCurrentIndex(index)
        self.tabChange(index)

    def tabChange(self, index):
        #This function is called whenever a parameter 
        self.tab_index = index #self.param_tabs.currentIndex()
        self.activeParameter = self.param_tabs.tabText(self.tab_index)
        print("Active Parameter = ", self.activeParameter)
        if self.selected:
            sample = self.selected[0]
        else:
            return
        #print index
        
        if self.tab_index >= 1:
            if sample.__repr__() == "Embed":
                tab_index = self.param_tabs.currentIndex()
                activeParameter = self.param_tabs.tabText(self.tab_index)
                self.embeddingWidget.embedPlotUpdate(activeParameter)

            if sample.__repr__() == "Plug":
                tab_index = self.param_tabs.currentIndex()
                activeParameter = self.param_tabs.tabText(self.tab_index)
                self.plugWidget.plugPlotUpdate(activeParameter)

            elif sample.__repr__() == "Alien":
                try: 
                    self.alienWidget
                except AttributeError: 
                    self.alienWidget = None
                if self.alienWidget is None:
                    self.setupAlien()
                self.alienWidget.alienPlotUpdate()

            elif sample.__repr__() == "SNP":
                currentParamWidget = self.paramWidgetList[self.tab_index]
                currentParamWidget.plotUpdate(sample, self.activeParameter)
            
                #print(self.sample.frequency.unit)

                #worstValue = sample.getWorstValue(self.activeParameter)
                #print(worstValue)

        else:
            self.plot(None, None)

    def setupMainTab(self):
        self.mainTabWidget.testNameLabel.setText(self.sample.name+" : ")
        self.mainTabWidget.dateLabel.setText(self.sample.date.__str__())
        self.mainTabWidget.limitLabel.setText(self.sample.standard.__str__())

    def connect(self):

        connectDialog =  ConnectDialog(self.comm)
        res=connectDialog.showDialog()  

        if res and self.comm._connected:
            if connectDialog.calib is False:
                self.comm.setCal(connectDialog.newDial.typeBox.currentIndex())
            self.actionWho_am_I.setEnabled(True)
            self.actionCalibrate.setEnabled(True)
            self.actionCalibrate_2.setEnabled(True)
            self.actionDisconnect.setEnabled(True)
            self.actionConnect.setEnabled(False)
            
            self.actionMeasure.setEnabled(True)
            self.actionRun.setEnabled(True)



    def disconnect(self):
        self.comm.disconnect()
        self.actionMeasure.setEnabled(False)
        self.actionWho_am_I.setEnabled(False)
        self.actionCalibrate.setEnabled(False)
        self.actionCalibrate_2.setEnabled(False)
        self.actionDisconnect.setEnabled(False)
        self.actionRun.setEnabled(False)
        self.actionConnect.setEnabled(True)


    def whoAmI(self):
        self.comm.whoAmI()

    def aquire(self):

        try:
            vnaDialog = VNATestDialog()
            res = vnaDialog.exec_()
            if res:
                name = vnaDialog.getSampleName()
                ports = vnaDialog.getPorts()
                sample_file = self.comm.acquire(name, ports, vnaDialog.getVNACOnfiguration())
                print(sample_file)
                self.Project.importSNP([sample_file])
                self.displaySamplesInTable()
        except Exception as e:
            print(e)


        '''try:
            
            if file:=self.comm.aquireInterface():

                self.Project.importSNP([file])
                self.displaySamplesInTable()

        except Exception as e:
            print(e)'''
            

    def simpleAquire(self):
        pass

    def reject(self):
        pass

    def calibrate(self):
        print("CALIBRATE")
        self.comm.calibrate()

    def setupConsole(self):
        self.consoleWidget = ConsoleWidget(parent = self.console_widget)
        sys.stdout = EmittingStream(textWritten=self.consoleWidget.writeToConsole)  # test
    
    def __del__(self):  # test
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

class Addr_Dialog:
    def getAddr(self):
        self.comm = Communication()
        dialog = QtWidgets.QDialog()
        addr_dialog = VNA_addr_dialog.Ui_Addr_Dialog()
        addr_dialog.setupUi(dialog)
        addr_dialog.plainTextEdit.setPlainText(self.comm.VNAAddress)

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

'''from UI import port_renumber
class Port_Renumbering:
    def getPortNumbering(self, fromPort):
        dialog = QtWidgets.QDialog()
        pr = port_renumber.Ui_Dialog()
        pr.setupUi(dialog)
        result = dialog.exec_()
        _from = None
        _to = None
        if not result:
            return None, None
        if result:
            _from = pr.fromLineEdit.text()
            _to = pr.toLineEdit.text()
            print("sent")
            if len(_from) < 1 or len(_to) < 1:
                return None, None
            return _from, _to'''





def main():

    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    app.setStyle('fusion')
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    #pixmap = QtGui.QPixmap("splash.jpeg")
    #splash = QtWidgets.QSplashScreen(pixmap)
    #splash.show()

    #time.sleep(10)
    form = BeldenSNPApp()  # We set the  form to be our ExampleApp (design)

    #form.show()  # Show the form
    form.showMaximized()

    print("Starting")
    print(sys.argv)
    '''sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    #splash.finish(form)

    sys.exit(app.exec_())'''
    app.exec_()
    app.deleteLater()        


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function


