from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets

from calibration import Calibration

import time


import visa
import pyvisa
class QIComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None):
        super(QIComboBox, self).__init__(parent)
 
 
class CalWizard(QtWidgets.QWizard):
    def __init__(self, comm, parent=None):
        
        super(CalWizard, self).__init__(parent)

        self.cal = Calibration(comm.session)
        time.sleep(3)
        print("Calibrting")

        #Define thru sequences in a dictioniary              
        self.thruOneEnd = {"1A":{"seq1":{"end1":[(1,2), (3,4), (5,6), (7,8)],"end2":[(9,10), (11,12), (13,14), (15,16)]}},
                      "2A":{"seq1":{"end1":[(1,3), (2,4)],  "end2":[(9,11), (10,12)]},
                            "seq2":{"end1":[(3,5),(4,6)],   "end2":[(11,13), (12,14)]},
                            "seq3":{"end1":[(5,7), (6,8)],  "end2":[(13,15), (14,16)]},
                            "seq4":{"end1":[(1,7), (2,8)],  "end2":[(9,15), (10,16)]}},
                      "3A":{"seq1":{"end1":[(1,4), (2,3)],  "end2":[(9,12), (10,11)]},
                            "seq2":{"end1":[(3,6),(4,5)],   "end2":[(11,14), (12,13)]},
                            "seq3":{"end1":[(5,8), (6,7)],  "end2":[(13,16), (14,15)]},
                            "seq4":{"end1":[(1,8), (2,7)],  "end2":[(9,16), (10,15)]}},
                      "4A":{"seq1":{"end1":[(1,5), (2,6)],  "end2":[(9,13), (10,14)]},
                            "seq2":{"end1":[(3,7),(4,8)],   "end2":[(11,15), (12,16)]}},
                      "5A":{"seq1":{"end1":[(1,6),(2,5)],  "end2":[(9,14), (10,13)]},
                            "seq2":{"end1":[(3,8),(4,7)],   "end2":[(11,16), (12,15)]}}}

        self.thruTwoEnd = {"2B":{"seq1":[(1,11), (2,12)],
                            "seq2":[(3,13), (4,14)],
                            "seq3":[(5,15), (6,16)],
                            "seq4":[(7,9), (8,10)]},
                      "3B":{"seq1":[(1,12), (2,11)],
                            "seq2":[(3,14), (4,13)],
                            "seq3":[(5,16), (6,15)],
                            "seq4":[(7,10), (8,9)]},
                      "4B":{"seq1":[(1,13), (2,14)],
                            "seq2":[(3,15), (4,16)],
                            "seq3":[(5,9), (6,10)],
                            "seq4":[(7,11),(8,12)]},
                      "5B":{"seq1":[(1,14), (2,13)],
                            "seq2":[(3,16), (4,15)],
                            "seq3":[(5,10), (6,9)],
                            "seq4":[(7,12), (8,11)]}}
        
        self.setWindowTitle("Cal Wizard")

        self.addPage(self.Intro())
        self.addPage(self.Open())
        self.addPage(self.Short())
        self.addPage(self.Load())
        for attach in self.thruOneEnd:
            for seq in self.thruOneEnd[attach]:
                self.addPage(self.Thru1E(attach, seq))

        if self.cal.numPorts == 16:
            for attach in self.thruTwoEnd:
                for seq in self.thruTwoEnd[attach]:
                    self.addPage(self.Thru2E(attach, seq))

        self.addPage(self.Finished())
                
        #self.button(self.NextButton).clicked.connect(self.nextButtonAction)
        self.button(self.FinishButton).clicked.connect(self.finishButtonAction)

        self.resize(640,480)

    def Intro(self):
        page = QtWidgets.QWizardPage()
        page.setTitle("<h1>Calibration Wizard<\h1>")
        self.label = QtWidgets.QLabel('''This wizard will guide you through the calibration of your VNA. The calibration is done on
all activated ports which were selected in the Keysight Network Analyzer software.

Before starting, please ensure that your OPEN, SHORT, LOAD and THRU arifacts are ready.

To begin calibration, click Next''')
        self.label.setWordWrap(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        page.setLayout(layout)
        print("Intro")

        return page
 

    def Open(self):
        page = QtWidgets.QWizardPage()
        page.setTitle("Open")
        self.label = QtWidgets.QLabel('''Insert Open artifact(s) onto VNA end(s)

Press Next once you've done so''')
        self.label.setWordWrap(True)
        self.openButton = QtWidgets.QPushButton("Calibrate Open", self);
        self.openButton.clicked.connect(self.OpenButtonAction)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.openButton)
        

        page.setLayout(layout)

        return page
 


    def Short(self):
        page = QtWidgets.QWizardPage()
        page.setTitle("Short")
        self.label = QtWidgets.QLabel('''Insert Short artifact(s) onto VNA end(s)

Press Next once you've done so''')
        self.label.setWordWrap(True)
        self.shortButton = QtWidgets.QPushButton("Calibrate Short", self);
        self.shortButton.clicked.connect(self.ShortButtonAction)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.shortButton)

        page.setLayout(layout)

        
        return page


    def Load(self):
        page = QtWidgets.QWizardPage()
        page.setTitle("Load")
        self.label = QtWidgets.QLabel('''Insert Load artifact(s) onto VNA end(s)

Press Next once you've done so''')
        self.label.setWordWrap(True)
        self.loadButton = QtWidgets.QPushButton("Calibrate Load", self);
        self.loadButton.clicked.connect(self.LoadButtonAction)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.loadButton)

        page.setLayout(layout)
        
        return page

    def Thru1E(self, attach, seq):   #Thru 1 end
        page = QtWidgets.QWizardPage()
        page.setTitle("Thru One end,{},{}".format(attach, seq))
        self.label = QtWidgets.QLabel('''Insert Thru artifact {} To make connections

{} - end1
{} - end2

Press Next once you've done so'''.format(attach,  str(self.thruOneEnd[attach][seq]["end1"]),  str(self.thruOneEnd[attach][seq]["end2"])))
        self.label.setWordWrap(True)
        self.thru1EButton = QtWidgets.QPushButton("Calibrate Thru 1 ended", self);
        self.thru1EButton.clicked.connect(self.Thru1EButtonAction)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.thru1EButton)

        page.setLayout(layout)

        #self.thruOut = self.thruOneEnd[attach][seq]
        
        return page


    def Thru2E(self, attach, seq):   #Thru 2 end
        page = QtWidgets.QWizardPage()
        page.setTitle("Thru Two end,{},{}".format(attach, seq))
        self.label = QtWidgets.QLabel('''Insert Thru artifact {} To make connections

{}

Press Next once you've done so'''.format(attach,  str(self.thruTwoEnd[attach][seq])))
        self.label.setWordWrap(True)
        self.thru2EButton = QtWidgets.QPushButton("Calibrate Thru 2 ended", self);
        self.thru2EButton.clicked.connect(self.Thru2EButtonAction)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.thru2EButton)

        page.setLayout(layout)

        print("Cal here")

        self.thruOut = self.thruTwoEnd[attach][seq]

        
        return page


    def Finished(self):
        page = QtWidgets.QWizardPage()
        page.setTitle("Finished")
        self.label = QtWidgets.QLabel('''Click Finished to Save Calibration''')
        self.label.setWordWrap(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        page.setLayout(layout)

        
        return page        
    
    def OpenButtonAction(self):
        title =  self.currentPage().title()
        print(title)
        print("SKIP")
        self.cal.openCalib()
        
            
    def ShortButtonAction(self):
        title =  self.currentPage().title()
        print(title)
        print("SKIP")
        self.cal.shortCalib()
        
    def LoadButtonAction(self):
        title =  self.currentPage().title()
        print(title)
        print("SKIP")
        self.cal.loadCalib()

    def Thru1EButtonAction(self):
        title =  self.currentPage().title()
        print(title)
        print("SKIP")
        attach = title.split(",")[1]
        seq = title.split(",")[2]
        self.thruOut = self.thruOneEnd[attach][seq]
        for end in self.thruOut:
            self.cal.thruCalib(self.thruOut[end])

    def Thru2EButtonAction(self):
        title =  self.currentPage().title()
        print(title)
        print("SKIP")
        attach = title.split(",")[1]
        seq = title.split(",")[2]
        self.thruOut = self.thruTwoEnd[attach][seq]
        self.cal.thruCalib(self.thruOut)
    
    def finishButtonAction(self):
         self.cal.save()
         self.cal.close()

if __name__ == '__main__':
    import sys
    import visa
    import pyvisa
    app = QtWidgets.QApplication(sys.argv)
    VISA_ADDRESS  = "TCPIP0::10.29.48.46::hislip0::INSTR"
    timeout = 50000
    rm = visa.ResourceManager()
    session = rm.open_resource(VISA_ADDRESS)
    session.timeout = timeout
    
    wizard = CalWizard()
    wizard.show()
    sys.exit(app.exec_())
