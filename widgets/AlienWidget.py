from UI import alienWidget as AW
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox, QListWidgetItem
from PyQt5.Qt import Qt


import matplotlib

from matplotlib.pyplot import cm
import numpy as np  
import os    
class AlienWidget():    
    def __init__(self, parentTab, graph, sample, comm=None):

        print("Alien Sample Added")

        self.comm = comm

        self.alienSample = sample

        self.parentTab = parentTab
        
        self.graphicsView = graph

        self.curPlot = None
        self.disturberList = dict()
        self.disturberList['end1'] = dict()
        self.disturberList['end2'] = dict()
        self.disturberList['end1']["ANEXT"] = []
        self.disturberList['end1']["AFEXT"] = []
        self.disturberList['end2']["ANEXT"] = []
        self.disturberList['end2']["AFEXT"] = []

        self.parentTab.clear()

        self.alienTab = QtWidgets.QWidget()

        self.alienWidget = AW.Ui_Form()
        self.parentTab.addTab(self.alienTab, "Alien")
        self.alienWidget.setupUi(self.alienTab)
        
        self.alienWidget.alienNear.setChecked(True)
        self.alienWidget.alienEnd1.setChecked(True)

        self.alienWidget.alienVictimButton.clicked.connect(self.alienImportVictimSNP)
        #self.alienWidget.alienDisturberButton.clicked.connect(self.alienAddDisturber)
        self.alienWidget.alienImportSNP.clicked.connect(self.alienImportSNP)
        self.alienWidget.alienRun.clicked.connect(self.alienRun)
        
        self.alienWidget.alienDisturbers.itemChanged.connect(self.updateSelectedDisturbers) 
        self.alienWidget.plotList.itemPressed.connect(self.setSelectedPlot)
        self.alienWidget.alienNear.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienFar.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienEnd1.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienEnd2.toggled.connect(self.alienRadioChange)

        '''self.alienWidget.alien12.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alien36.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alien45.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alien78.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alienAvg.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alienLimitCheck.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alienAvgLimitCheck.toggled.connect(self.alienPlotUpdate)'''

        #self.alienUpdateDisturberList()
        
        self.selectedPlot = None
        self.plotTitle = None
        self.alienRadioChange()
        try: 
            self.updatePlotsList()
        except:
            pass
        #self.alienUpdateDisturberList()
        self.alienPlotUpdate()

    


    def alienRadioChange(self):

        if self.alienWidget.alienEnd1.isChecked():
            self.end = "end1"
        elif self.alienWidget.alienEnd2.isChecked():
            self.end = "end2"
            
        if self.alienWidget.alienNear.isChecked():
            self.testType = "ANEXT"
        elif self.alienWidget.alienFar.isChecked():
            self.testType = "AFEXT"


        self.alienUpdateDisturberList()
        self.updatePlotsList()
        self.alienPlotUpdate()

    def updatePlotsList(self):
        while self.alienWidget.plotList.count() > 0:
            self.alienWidget.plotList.takeItem(0)
        
        if self.testType == "ANEXT":
            testType = "near-end"
            aarcType = "ACRN"
        if self.testType == "AFEXT":
            testType = "far-end"
            aarcType = "ACRF"

        if self.alienSample.disturbedSNP is not None:
            vicItem = QListWidgetItem()
            vicItem.setText("Victim - IL")
            vicItem.setData(Qt.UserRole, "Victim")
            self.alienWidget.plotList.addItem(vicItem)

        if len(self.alienSample.PSAlien[self.end][self.testType]) :
            PSItem = QListWidgetItem()
            PSItem.setText(f"Power sum alien {testType} crosstalk (PS{self.testType}) ")
            PSItem.setData(Qt.UserRole, (self.end, self.testType, "PSAlien"))
            self.alienWidget.plotList.addItem(PSItem)

        if len(self.alienSample.PSAACRX[self.end][self.testType]):
            PSItem = QListWidgetItem()
            PSItem.setText(f"Power sum attenuation  to alien crosstalk ratio, {testType} (PSA{aarcType}) ")
            PSItem.setData(Qt.UserRole, (self.end, self.testType, "PSAACRX"))
            self.alienWidget.plotList.addItem(PSItem)

        

            #self.alienWidget.plotList.addItem(chkBoxItem)
        
    def updateSelectedDisturbers(self):
        alien = self.alienSample

        for i in range(self.alienWidget.alienDisturbers.count()):
            dist = self.alienWidget.alienDisturbers.item(i)
            if dist.checkState():
                self.disturberList[self.end][self.testType].append(dist.text())
            else:
                if dist.text() in self.disturberList[self.end][self.testType]:
                    self.disturberList[self.end][self.testType].remove(dist.text())

        
        #if len(disturberList):
        alien.getPSAlien(self.end, self.testType, self.disturberList[self.end][self.testType]) #Calculate PSAFEXT
        alien.getPSAACRX(self.end, self.testType)
        self.alienPlotUpdate()


    def alienPlotUpdate(self):

        alien = self.alienSample

        disturberList = []
        limit = None
        avgLimit = None
        if alien.standard and len(alien.freq):
            if self.alienWidget.alienNear.isChecked():
                if self.alienWidget.alienLimitCheck.isChecked():
                    limit = alien.standard.limits["PSANEXT"].getArray()#evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
                if self.alienWidget.alienAvgLimitCheck.isChecked():
                    avgLimit = alien.standard.limits["AVGPSANEXT"].getArray()#.evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
            elif self.alienWidget.alienFar.isChecked():
                if self.alienWidget.alienLimitCheck.isChecked():
                    limit = alien.standard.limits["PSAACRF"].getArray()#.evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
                if self.alienWidget.alienAvgLimitCheck.isChecked():
                    avgLimit = alien.standard.limits["AVGPSAACRF"].getArray()#.evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)


        #print(self.selectedPlot)
        if self.selectedPlot is not None:
            #print("Ploting")
            self.plot(alien.freq, self.selectedPlot, limit=limit, avgLimit=avgLimit, title = self.plotTitle)
        else:
            print("No selected plot")
      
    def alienImportVictimSNP(self):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            #print(file)
            alien = self.alienSample
            alien.addDisturbed(file)
            self.alienUpdateDisturberList()
            #self.alienPlotUpdate()

        self.updatePlotsList()

    """def alienAddDisturber(self):
        print("Add Disturber")
        alien = self.alienSample

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
            alien = self.alienSample
            for file in files:
                name, extension = splitext(os.path.basename(file))
                alien.addDisturber(name)
                
            self.alienUpdateDisturberList()"""

    def alienUpdateDisturberList(self):


        alien = self.alienSample
        self.alienWidget.alienDisturbers.clear()
        end = self.end
        testType = self.testType

        #Firstly we must get if End1 or End2 is selected and if PSANEXT or PSAACRF is selected


        for disturber in alien.disturbers[end][testType].keys():
            item = QtWidgets.QListWidgetItem()
            item.setText(disturber)
            try:
                #print(alien.disturbers[disturber][end].keys())

                alien.disturbers[end][testType][disturber] #See if defined
            except Exception as e:
                pass
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                if disturber in self.disturberList[self.end][self.testType]:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)
            self.alienWidget.alienDisturbers.addItem(item)

            

    def alienRun(self):

        alien = self.alienSample

        if self.alienWidget.alienEnd1.isChecked():
            end = "end1"
        elif self.alienWidget.alienEnd2.isChecked():
            end = "end2"
            
        if self.alienWidget.alienNear.isChecked():
            testType = "ANEXT"
        elif self.alienWidget.alienFar.isChecked():
            testType = "AFEXT"
        try:
               
            f = self.comm.aquireInterface()

            import os.path
            alien.addDisturberMeasurement(end, testType, f, os.path.basename(f))
            self.alienUpdateDisturberList()
            self.alienPlotUpdate()
            
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please Connect to VNA ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()
                   

    def alienImportSNP(self):
        
        alien = self.alienSample

        end = self.end
        testType = self.testType

        #try:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)

        #import os.path
        for file in files:
            #print(file, os.path.basename(file))
            alien.addDisturberMeasurement(end, testType, file, os.path.basename(file))
            self.disturberList[self.end][self.testType].append(os.path.basename(file))
        
        self.alienUpdateDisturberList()
        self.updateSelectedDisturbers()

        self.updatePlotsList()

        self.alienPlotUpdate()
            
        '''except Exception as e:
            print("alien import snp : ", e)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please select disturber to add ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()'''


    def plot(self, x=None, param_dict=None, limit = None, unit = "Mhz", avgLimit = None, title=None):

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
            ax.set_title(title)

            if limit is not None:
                ax.semilogx(*zip(*limit), linestyle = '--', label="limit", c = c)

            if avgLimit is not None:
                ax.semilogx(*zip(*avgLimit), linestyle = '--', label="average limit", c = c)
            ax.legend(loc='upper left', ncol = 1 if len(param_dict.keys()) <= 8 else 2 )
     
            #self.ax.legend()
        self.graphicsView.draw()

    def setSelectedPlot(self, item):
        self.plotTitle = ""
        print(item.data(Qt.UserRole))
        if item.data(Qt.UserRole) == "Victim":
            self.selectedPlot = self.alienSample.distrubedIL
            #print(self.selectedPlot)
            self.plotTitle = "Victim - IL"
        else:
            end, testType, PS = item.data(Qt.UserRole)
            if PS == "PSAlien":
                self.selectedPlot = self.alienSample.PSAlien[end][testType]

            if PS == "PSAACRX":
                self.selectedPlot = self.alienSample.PSAACRX[end][testType]
                 
            self.plotTile = PS + ", " + end


        self.alienPlotUpdate()