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

import alienWidget
import embedWidget

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

from decimal import Decimal

class BeldenSNPApp(QtWidgets.QMainWindow, MW3.Ui_MainWindow, QtWidgets.QAction, QtWidgets.QFileDialog, QtWidgets.QListView, QtWidgets.QDialog, QtCore.Qt):

    '''
    This class handles all of the user sent commands from the GUI.   

    '''

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

        self.activeParameter = "Main" #We want the the first sample tab to display to be the Main tab.
                                                                            

        nav = NavigationToolbar(self.graphicsView, self)  #Sets up the menu at the bottom of the GUI which lets us interact with the matplotlib plots
        self.verticalLayout_3.addWidget(nav)


        #Here, we process any arguments that might be sent the program from outside of the interface.
        #In other words, when ever a user right click on an SNP files, rather than opening them in Notepad, it would be opened in this interface.
        arguments = sys.argv[1:] 
        
        if len(arguments):
            self.Project.importSNP(arguments)
            self.displaySamplesInTable()
            

    def importSnp(self):
        #Whenever the user clicks on the import SNP button, it opens a file dialog
        self.openFileNamesDialog()


    def addEmbed(self):
        testName, result = QtWidgets.QInputDialog.getText(self, "Add an Embedded Sample",
                                                                "Please enter a sample name")
        if result and len(testName) > 1 and not testName.isspace():
            print("%s!" % testName)
            self.Project.addEmbed(testName)
            self.displaySamplesInTable()
        else:
            return
        
    def addAlien(self):

        self.Project.addAlien("Test")
        self.displaySamplesInTable()

    def newProject(self):
        
        self.Project = Project()
        self.sampleTable.setRowCount(0);

    def deleteSample(self):
        
        self.Project.delete(self.selected)
        self.displaySamplesInTable()
        self.setActiveSample()

    def setLimit(self):
        pass

    def setActiveSample(self):
        self.plot(None, None)

        self.selected = []
        for i in self.sampleTable.selectionModel().selectedRows():
            self.selected.append(self.sampleTable.item(i.row(),0).text())
        #print self.selected
        if len(self.selected) >= 1:
            self.Project.activeSample = self.selected
           
        
        if len(self.selected) == 1:  #Since only one sample can be displayed at a time

            if self.Project.getSampleByName(self.selected[0]).__retr__() == "Alien":
                self.setupAlien()

            elif self.Project.getSampleByName(self.selected[0]).__retr__() == "Embed":
                self.setupEmbed()

            else:
                self.displaySampleParams(self.selected)
        
        elif len(self.selected) > 1 or len(self.selected) < 1:
            self.displaySampleParams(None)


    def displaySamplesInTable(self):
        measurementCount = len(self.Project.measurements)
        self.sampleTable.setRowCount(measurementCount)
        for i in range(0, measurementCount):
            self.sampleTable.setItem(i, 0, QtWidgets.QTableWidgetItem(self.Project.measurements[i].name))
            self.sampleTable.setItem(i, 1, QtWidgets.QTableWidgetItem(self.Project.measurements[i].date))
            self.sampleTable.setItem(i, 2, QtWidgets.QTableWidgetItem(self.Project.measurements[i].limit))
        self.sampleTable.resizeColumnsToContents()
        
    
    def setupEmbed(self):
        print("Embedding Sample Added")
        self.param_tabs.clear()

        self.embeddingTab = QtWidgets.QWidget()
        self.TPNextPhaseTab = QtWidgets.QWidget()

        self.embedWidget = embedWidget.Ui_Form()
        #self.param_tabs.addTab(self.TPNextPhaseTab, "TP NEXT phase")        

        self.embedWidget.setupUi(self.embeddingTab)

        self.embedWidget.embedCat6.setChecked(True)

        self.embedWidget.importOpen.clicked.connect(self.importOpen)
        self.embedWidget.importShort.clicked.connect(self.importShort)
        self.embedWidget.importLoad.clicked.connect(self.importLoad)
        self.embedWidget.reembedButton.clicked.connect(self.reembed)
        self.embedWidget.plugList.currentIndexChanged.connect(self.embedUpdatePlugDNEXT)
        
        self.embedWidget.reverseCheckBox.toggled.connect(self.embedUpdateTab)
       
        self.embedUpdateTab()

    def embedUpdatePlugDNEXT(self):
        embeddedSample = self.Project.getSampleByName(self.selected[0])

        plugIndex = self.embedWidget.plugList.currentIndex()
        plug = embeddedSample.getPlugList()[plugIndex]
        plugFile = plug + ".xml"

        embeddedSample.getPlugParams(plugFile)
        print(embeddedSample.plugNextDelay)
        self.embedWidget.dnext12_36.setText(str(embeddedSample.plugNextDelay["12-36"]))
        self.embedWidget.dnext45_12.setText(str(embeddedSample.plugNextDelay["45-12"]))
        self.embedWidget.dnext12_78.setText(str(embeddedSample.plugNextDelay["12-78"]))
        self.embedWidget.dnext45_36.setText(str(embeddedSample.plugNextDelay["45-36"]))
        self.embedWidget.dnext36_78.setText(str(embeddedSample.plugNextDelay["36-78"]))
        self.embedWidget.dnext45_78.setText(str(embeddedSample.plugNextDelay["45-78"]))
        
    def importOpen(self):
        embeddedSample = self.Project.getSampleByName(self.selected[0])
        embeddedSample.embeddedOpen = self.embedImportSNP()
        self.embedUpdateTab()

    def importShort(self):
        embeddedSample = self.Project.getSampleByName(self.selected[0])
        embeddedSample.embeddedShort = self.embedImportSNP()
        self.embedUpdateTab()
        
    def importLoad(self):
        embeddedSample = self.Project.getSampleByName(self.selected[0])
        embeddedSample.embeddedLoad = self.embedImportSNP()
        self.embedUpdateTab()
        
    def reembed(self):
        embeddedSample = self.Project.getSampleByName(self.selected[0])
        plugIndex = self.embedWidget.plugList.currentIndex()
        plug = embeddedSample.getPlugList()[plugIndex]
        plugFile = plug + ".xml"

        embeddedSample.getPlugParams(plugFile)

        embeddedSample.k1 = self.embedWidget.SJ_124578_LineEdit.text()
        embeddedSample.k2 = self.embedWidget.sJ36LineEdit.text()
        embeddedSample.k3 = self.embedWidget.thruCalibLineEdit.text()

        print(embeddedSample.k1)

        if self.embedtestType == "Reverse":
            print(embeddedSample.embeddedOpen)
            if embeddedSample.embeddedOpen.isspace() or embeddedSample.embeddedShort.isspace() or embeddedSample.embeddedLoad.isspace():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Make sure that you have selected an open, short and load sample")
                msg.setWindowTitle("Reverse file missing")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setFixedSize(msg.sizeHint())
                msg.exec_()                
            else:
                embeddedSample.getJackVectorReverse(embeddedSample.embeddedOpen, embeddedSample.embeddedShort, embeddedSample.embeddedLoad)
                embeddedSample.reembed()
                self.embedUpdateTab()

        else:
            if embeddedSample.embeddedLoad.isspace():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Make sure that you have selected a load sample")
                msg.setWindowTitle("Forward file missing")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setFixedSize(msg.sizeHint())
                msg.exec_()
            else:
                embeddedSample.getJackVector(embeddedSample.embeddedLoad)
                embeddedSample.reembed()
                self.embedUpdateTab()

        #embeddedSample.reembed()
        #self.embedUpdateTab()
        '''self.embedPlugUpdate()'''
        
    
    def embedImportSNP(self):
        
        options = self.Options()
        options |= self.DontUseNativeDialog
        file, _ = self.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            return file

    def embedUpdateTab(self):
        embeddedSample = self.Project.getSampleByName(self.selected[0])

        plugIndex = self.embedWidget.plugList.currentIndex()
        plug = embeddedSample.getPlugList()[plugIndex]
        plugFile = plug + ".xml"

        embeddedSample.getPlugParams(plugFile)

        self.embedWidget.openFileName.setText(embeddedSample.embeddedOpen)
        self.embedWidget.shortFileName.setText(embeddedSample.embeddedShort)
        self.embedWidget.loadFileName.setText(embeddedSample.embeddedLoad)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.embedWidget.openFileName.setFont(font)
        self.embedWidget.shortFileName.setFont(font)
        self.embedWidget.loadFileName.setFont(font)


        plugs = embeddedSample.getPlugList()
        
        self.embedWidget.plugList.clear()

        self.embedWidget.plugList.addItems(plugs)

        self.param_tabs.clear()

        self.param_tabs.addTab(self.embeddingTab, "Embedding Main")

        embededParams = embeddedSample.getParameters()
        print(embededParams)

        if bool(embeddedSample.reembeded):

            self.embeded_tab_list = []

            for key in embededParams.keys():
                self.new_Embededtab = QtWidgets.QWidget()
                self.embeded_tab_list.append(self.new_Embededtab)
                self.param_tabs.addTab(self.new_Embededtab, key)
                
        if self.embedWidget.reverseCheckBox.isChecked():
            self.embedtestType = "Reverse"
            self.embedWidget.importOpen.setEnabled(True)
            self.embedWidget.acquireOpen.setEnabled(True)
            self.embedWidget.importShort.setEnabled(True)
            self.embedWidget.acquireShort.setEnabled(True)

        else:
            self.embedtestType = "Forward"
            self.embedWidget.importOpen.setEnabled(False)
            self.embedWidget.acquireOpen.setEnabled(False)
            self.embedWidget.importShort.setEnabled(False)
            self.embedWidget.acquireShort.setEnabled(False)

        self.embedWidget.SJ_124578_LineEdit.setText(str(embeddedSample.k1))
        self.embedWidget.sJ36LineEdit.setText(str(embeddedSample.k2))
        self.embedWidget.thruCalibLineEdit.setText(str(embeddedSample.k3))


    def embedPlotUpdate(self):

        tab_index = self.param_tabs.currentIndex()
        activeParameter = self.param_tabs.tabText(self.tab_index)
        print(self.activeParameter)
        sample = self.Project.getSampleByName(self.selected[0])
        embeddedSample = self.Project.getSampleByName(self.selected[0])

        embededParams = embeddedSample.getParameters()

        if activeParameter != "Embedding Main":
            self.graphicsView.figure.clear()

            if activeParameter not in embededParams.keys():
                return
            
            ax=self.graphicsView.figure.add_subplot(111)
            
            color=iter(cm.rainbow(np.linspace(0,1,len(embededParams[activeParameter]))))
            for case in embededParams[activeParameter]:
                c = next(color)
                reembedingNum = int(case.replace("case", ""))
                ax.semilogx(sample.freq, sample.reembeded[reembedingNum], label=case, c = c)
                
            ax.legend(loc='upper left', ncol =  2 )

            #self.figure.tight_layout()

            ax.grid(which="both")

            ax.set_xlabel('Freq (Hz)')
            ax.set_ylabel('dB')
            ax.set_title(activeParameter)

                
            #self.ax.legend()
            self.graphicsView.draw()
        else:
            self.plot(None, None)       

                
        
    def setupAlien(self):
        print("Alien Sample Added")
        self.param_tabs.clear()

        self.alienTab = QtWidgets.QWidget()

        self.alienWidget = alienWidget.Ui_Form()
        self.param_tabs.addTab(self.alienTab, "Alien")
        self.alienWidget.setupUi(self.alienTab)
        self.alienUpdateDisturberList()
        
        self.alienWidget.alienPSANEXT.setChecked(True)
        self.alienWidget.alienEnd1.setChecked(True)

        self.alienWidget.alienVictimButton.clicked.connect(self.alienImportVictimSNP)
        self.alienWidget.alienDisturberButton.clicked.connect(self.alienAddDisturber)
        self.alienWidget.alienImportSNP.clicked.connect(self.alienImportSNP)
        self.alienWidget.alienDisturbers.itemChanged.connect(self.alienPlot) 
        
        self.alienWidget.alienPSANEXT.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienPSAACRF.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienEnd1.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienEnd2.toggled.connect(self.alienRadioChange)

        self.alienWidget.alien12.toggled.connect(self.alienPlot)
        self.alienWidget.alien36.toggled.connect(self.alienPlot)
        self.alienWidget.alien45.toggled.connect(self.alienPlot)
        self.alienWidget.alien78.toggled.connect(self.alienPlot)
        self.alienWidget.alienAvg.toggled.connect(self.alienPlot)

        self.alienUpdateDisturberList()
        self.alienPlot()


    def alienRadioChange(self):
        self.alienUpdateDisturberList()
        self.alienPlot()
        
    def alienPlot(self):

        alien = self.Project.getSampleByName(self.selected[0])

        disturberList = []

        for i in range(self.alienWidget.alienDisturbers.count()):
            dist = self.alienWidget.alienDisturbers.item(i)
            if dist.checkState():
                disturberList.append(dist.text())
            else:
                print("N")
        try:
            if self.alienWidget.alienEnd1.isChecked():
                end = "end1"
            elif self.alienWidget.alienEnd2.isChecked():
                end = "end2"
                
            if self.alienWidget.alienPSANEXT.isChecked():
                testType = "ANEXT"
                PS = alien.getPSAlien(end, testType, disturberList)
            elif self.alienWidget.alienPSAACRF.isChecked():
                testType = "PSAFEXT"
                alien.getPSAlien(end, "AFEXT", disturberList) #Calculate PSAFEXT
                PS = alien.getPSAACRX(end, testType)
                
            alienPlots = {}
            
            if self.alienWidget.alien12.isChecked():
                alienPlots["12"] = PS["12"]
            if self.alienWidget.alien36.isChecked():
                alienPlots["36"] = PS["36"]
            if self.alienWidget.alien45.isChecked():
                alienPlots["45"] = PS["45"]
            if self.alienWidget.alien78.isChecked():
                alienPlots["78"] = PS["78"]
            try:
                self.plot(alien.freq, alienPlots)
            except Exception as e:
                print("No Sample")

        except Exception as e:
            print("Error")
      
    def alienImportVictimSNP(self):
        
        options = self.Options()
        options |= self.DontUseNativeDialog
        file, _ = self.getOpenFileName(self,"QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            print(file)
            alien = self.Project.getSampleByName(self.selected[0])
            alien.addDisturbed(file)

    def alienAddDisturber(self):
        print("Add Disturber")
        alien = self.Project.getSampleByName(self.selected[0])

        '''dist, okPressed = QtWidgets.QInputDialog.getText(self, "Add disturber","Distuber ID:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and dist != '':
            print("Disturber added:", dist)
        alien.addDisturber(dist)'''
        options = self.Options()
        options |= self.DontUseNativeDialog
        files, _ = self.getOpenFileNames(self,"Select Disturbers", "", "sNp Files (*.s*p)", options=options)
        #print files
        if files:
            print(files)
            alien = self.Project.getSampleByName(self.selected[0])
            for file in files:
                name, extension = splitext(os.path.basename(file))
                alien.addDisturber(name)
                
            self.alienUpdateDisturberList()

    def alienUpdateDisturberList(self):
        alien = self.Project.getSampleByName(self.selected[0])
        self.alienWidget.alienDisturbers.clear()

        #Firstly we must get if End1 or End2 is selected and if PSANEXT or PSAACRF is selected

        if self.alienWidget.alienEnd1.isChecked():
            end = "end1"
        elif self.alienWidget.alienEnd2.isChecked():
            end = "end2"
            
        if self.alienWidget.alienPSANEXT.isChecked():
            testType = "ANEXT"
        elif self.alienWidget.alienPSAACRF.isChecked():
            testType = "AFEXT"

        for disturber in alien.disturbers.keys():
            item = QtWidgets.QListWidgetItem()
            item.setText(disturber)
            try:
                print(alien.disturbers[disturber][end].keys())

                alien.disturbers[disturber][end][testType] #See if defined
            except Exception as e:
                print("Doesnt Exist")
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
            self.alienWidget.alienDisturbers.addItem(item)
            

    def alienImportSNP(self):
        
        alien = self.Project.getSampleByName(self.selected[0])

        if self.alienWidget.alienEnd1.isChecked():
            end = "end1"
        elif self.alienWidget.alienEnd2.isChecked():
            end = "end2"
            
        if self.alienWidget.alienPSANEXT.isChecked():
            testType = "ANEXT"
        elif self.alienWidget.alienPSAACRF.isChecked():
            testType = "AFEXT"
        try:
            selectedDisturber = self.alienWidget.alienDisturbers.currentItem().text()

            print(selectedDisturber)

            try:
                alien.disturbers[selectedDisturber][end][testType] #See if defined
            except Exception as e:
                print("Sample doesnt have an SNP")
            else:
                print("Sample already has an attributed SNP file")
                
            options = self.Options()
            options |= self.DontUseNativeDialog
            file, _ = self.getOpenFileName(self,"Select ALlien test", "","sNp Files (*.s*p)", options=options)

            alien.addDisturberMeasurement(end, testType, file, selectedDisturber)
            self.alienUpdateDisturberList()
            self.alienPlot()
            
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please select disturber to add")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()
            
    def openFileNamesDialog(self):

        options = self.Options()
        options |= self.DontUseNativeDialog
        files, _ = self.getOpenFileNames(self, "Select SNP(s)", "","sNp Files (*.s*p)", options=options)
        #print files
        print(files)
        self.Project.importSNP(files)

        #print(self.rs.RL.items())
        #self.plot(self.rs.NEXT) USE THIS !!!!!!!

        self.displaySamplesInTable()

    def plot(self, x=None, param_dict=None):

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
                ax.semilogx(x, param_dict[key], label=key, c = c)
                #print key 

            ax.legend(loc='upper left', ncol = 1 if len(param_dict.keys()) <= 8 else 2 )

            #self.figure.tight_layout()

            ax.grid(which="both")

            ax.set_xlabel('Freq (Hz)')
            ax.set_ylabel('dB')
            ax.set_title(self.activeParameter)
            if self.activeParameter.replace(" ", "") == "PropagationDelay":
                ax.set_ylabel('nSec')
                
            #self.ax.legend()
        self.graphicsView.draw()
        

    def tableContextMenu(self, pos):
        #print self.selected

        if len(self.selected) > 0 and self.Project.getSampleByName(self.selected[0]).__retr__() == "SNP":
            #Start by getting info on the sample. (If they're all the same type or not)

            menu = QtWidgets.QMenu()
            setLimit = menu.addAction("Set Limit")
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
                    self.Project.getSampleByame(sample).reCalc(one_sided = False)

                if len(self.selected) == 1:  #Since only one sample can be displayed at a time
                    self.displaySampleParams(self.selected)

                elif len(self.selected) > 1:
                    self.displaySampleParams(None)

            elif action == exportExcel:
                print(self.selected)
                file, _ = self.getSaveFileName(self,"Export Excel Repport", "","Excel File (*.xlsx)")
                self.Project.generateExcel(file , self.selected, True)

            elif action == delete:
                self.deleteSample()

            #self.Project.activeMeasurements = selected
            return 1

        menu = QtWidgets.QMenu()
        addSNP = menu.addAction("Add Sample")
        addAlien = menu.addAction("Add Alien Sample")
        addEmbed = menu.addAction("Add Emdedding Sample")

        selectAll = menu.addAction("Select All")
        action = menu.exec_(QtGui.QCursor.pos())
        if action == selectAll:
            self.sampleTable.selectAll()
        elif action == addSNP:
            self.openFileNamesDialog()
        elif action == addAlien:
            self.addAlien()
        elif action == addEmbed:
            self.addEmbed()

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
            #print(param)
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
        #This function is called whenever a parameter 
        self.tab_index = self.param_tabs.currentIndex()
        self.activeParameter = self.param_tabs.tabText(self.tab_index)
        print(self.activeParameter)
        if self.selected:
            sample = self.Project.getSampleByName(self.selected[0])
        else:
            return
        #print index
        
        if self.tab_index >= 1:
            if sample.__retr__() == "Embed":
                self.embedPlotUpdate()
            else:
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
                    self.comm = Communication()
                    self.comm.connectToVNA(addr)
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
                    print("Error: ",e)
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
            try:
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
            except Exception as e:
                print("Cancel")

    def reject(self):
        pass

    def calibrate(self):
        print("CALIBRATE")
        self.comm.calibrate()

class Addr_Dialog:
    def getAddr(self):
        comm = Communication()
        dialog = QtWidgets.QDialog()
        addr_dialog = VNA_addr_dialog.Ui_Addr_Dialog()
        addr_dialog.setupUi(dialog)
        addr_dialog.plainTextEdit.setPlainText(comm.VNAAddress)

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

        comm = Communication()
        
        dialog = QtWidgets.QDialog()
        params_dialog = TestParameters.Ui_TestParameterDialog()
        params_dialog.setupUi(dialog)
        print("Current ID: ", comm.test_name)
        print("NEXT ID: ", comm.getNextID(comm.test_name))
        params_dialog.testNameLineEdit_2.setText(comm.getNextID(comm.test_name)) 
        params_dialog.iFBandwidthLineEdit.setText(str(comm.IF))
        print("Min Freq ", comm.min_freq)
        params_dialog.startFrequencyLineEdit.setText('%E' % Decimal(comm.min_freq))
        params_dialog.stopFrequencyLineEdit.setText('%E' % Decimal(comm.max_freq))
        params_dialog.numberOfPointsLineEdit.setText(str(comm.num_points))
        params_dialog.numberOfPortsLineEdit.setText(str(comm.port_num))
        params_dialog.numberOfAverageLineEdit.setText(str(comm.average))
        params_dialog.timeoutLineEdit.setText('%E' % Decimal(comm.timeout))

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
                print("Cancel")

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
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    #splash.finish(form)

    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function


