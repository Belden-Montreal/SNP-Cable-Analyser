from UI import alienWidget as AW
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox
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

        self.parentTab.clear()

        self.alienTab = QtWidgets.QWidget()

        self.alienWidget = AW.Ui_Form()
        self.parentTab.addTab(self.alienTab, "Alien")
        self.alienWidget.setupUi(self.alienTab)
        self.alienUpdateDisturberList()
        
        self.alienWidget.alienPSANEXT.setChecked(True)
        self.alienWidget.alienEnd1.setChecked(True)

        self.alienWidget.alienVictimButton.clicked.connect(self.alienImportVictimSNP)
        #self.alienWidget.alienDisturberButton.clicked.connect(self.alienAddDisturber)
        self.alienWidget.alienImportSNP.clicked.connect(self.alienImportSNP)
        self.alienWidget.alienRun.clicked.connect(self.alienRun)
        
        self.alienWidget.alienDisturbers.itemChanged.connect(self.alienPlotUpdate) 
        
        self.alienWidget.alienPSANEXT.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienPSAACRF.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienEnd1.toggled.connect(self.alienRadioChange)
        self.alienWidget.alienEnd2.toggled.connect(self.alienRadioChange)

        self.alienWidget.alien12.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alien36.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alien45.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alien78.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alienAvg.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alienLimitCheck.toggled.connect(self.alienPlotUpdate)
        self.alienWidget.alienAvgLimitCheck.toggled.connect(self.alienPlotUpdate)

        self.alienUpdateDisturberList()
        self.alienPlotUpdate()


    def alienRadioChange(self):
        self.alienUpdateDisturberList()
        self.alienPlotUpdate()
        
    def alienPlotUpdate(self):

        alien = self.alienSample

        disturberList = []
        limit = None
        avgLimit = None
        if alien.standard and len(alien.freq):
            if self.alienWidget.alienPSANEXT.isChecked():
                if self.alienWidget.alienLimitCheck.isChecked():
                    limit = alien.standard.limits["PSANEXT"].evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
                if self.alienWidget.alienAvgLimitCheck.isChecked():
                    avgLimit = alien.standard.limits["AVGPSANEXT"].evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
            elif self.alienWidget.alienPSAACRF.isChecked():
                if self.alienWidget.alienLimitCheck.isChecked():
                    limit = alien.standard.limits["PSAACRF"].evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
                if self.alienWidget.alienAvgLimitCheck.isChecked():
                    avgLimit = alien.standard.limits["AVGPSAACRF"].evaluateArray({'f': alien.freq}, len(alien.freq), neg=True)
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
            
            try:
                if self.alienWidget.alien12.isChecked():
                    alienPlots["12"] = PS["12"]
            except:
                pass
            try:
                if self.alienWidget.alien36.isChecked():
                    alienPlots["36"] = PS["36"]
            except:
                pass
            try:
                if self.alienWidget.alien45.isChecked():
                    alienPlots["45"] = PS["45"]
            except:
                pass
            try:
                if self.alienWidget.alien78.isChecked():
                    alienPlots["78"] = PS["78"]
            except:
                pass
            try:
                self.plot(alien.freq, alienPlots, limit=limit, avgLimit=avgLimit, title = testType + ',' + end)
            except Exception as e:
                print("Alien Plot Error :", e)

        except Exception as e:
            print("ALIEN ERROR : " ,e)
      
    def alienImportVictimSNP(self):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            print(file)
            alien = self.alienSample
            alien.addDisturbed(file)
            self.alienUpdateDisturberList()
            self.alienPlotUpdate()

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

        end = "end1"
        testType = "ANEXT"

        alien = self.alienSample
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

        print(end)
        print(testType)

        for disturber in alien.disturbers[end][testType].keys():
            item = QtWidgets.QListWidgetItem()
            item.setText(disturber)
            try:
                #print(alien.disturbers[disturber][end].keys())

                alien.disturbers[end][testType][disturber] #See if defined
            except Exception as e:
                print("Doesnt Exist")
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
            self.alienWidget.alienDisturbers.addItem(item)
            

    def alienRun(self):

        alien = self.alienSample

        if self.alienWidget.alienEnd1.isChecked():
            end = "end1"
        elif self.alienWidget.alienEnd2.isChecked():
            end = "end2"
            
        if self.alienWidget.alienPSANEXT.isChecked():
            testType = "ANEXT"
        elif self.alienWidget.alienPSAACRF.isChecked():
            testType = "AFEXT"
        try:
               
            f = self.comm.aquireInterface()
            print("here")
            import os.path
            print(f)
            alien.addDisturberMeasurement(end, testType, f, os.path.basename(f))
            self.alienUpdateDisturberList()
            self.alienPlotUpdate()
            
        except Exception as e:
            print(e)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please Connect to VNA ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()
                   

    def alienImportSNP(self):
        
        alien = self.alienSample

        if self.alienWidget.alienEnd1.isChecked():
            end = "end1"
        elif self.alienWidget.alienEnd2.isChecked():
            end = "end2"
            
        if self.alienWidget.alienPSANEXT.isChecked():
            testType = "ANEXT"
        elif self.alienWidget.alienPSAACRF.isChecked():
            testType = "AFEXT"
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)

            #import os.path
            for file in files:
                print(file, os.path.basename(file))
                alien.addDisturberMeasurement(end, testType, file, os.path.basename(file))
            self.alienUpdateDisturberList()
            self.alienPlotUpdate()
            
        except Exception as e:
            print("alien import snp : ", e)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please select disturber to add ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()


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