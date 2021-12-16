from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox
import widgets.PlugWidget as PlugWidget

from UI import embedWidget as EW
from matplotlib.pyplot import cm
import numpy as np

class EmbeddingWidget(QtWidgets.QWidget):
    proc_addPlug = QtCore.pyqtSignal()
    proc_importPlug = QtCore.pyqtSignal()

    def __init__(self, parentTab, graph, sample, comm=None, project = None):
        
        super(self.__class__, self).__init__()

        print("Embedding Sample Added")
        self.comm = comm

        self.embeddedSample = sample

        self.parentTab = parentTab
        
        self.graphicsView = graph

        self.project = project

        self.embeddingTab = QtWidgets.QWidget()
        #self.TPNextPhaseTab = QtWidgets.QWidget()

        self.embedWidget = EW.Ui_EmbeddingWidget()
        #self.parentTab.addTab(self.TPNextPhaseTab, "TP NEXT phase")        

        self.embedWidget.setupUi(self.embeddingTab)

        self.embedWidget.embedCat6.setChecked(True)

        self.embedWidget.importOpen.clicked.connect(self.importOpen)
        self.embedWidget.importShort.clicked.connect(self.importShort)
        self.embedWidget.importLoad.clicked.connect(self.importLoad)

        self.embedWidget.acquireOpen.clicked.connect(self.acquireOpen)
        self.embedWidget.acquireShort.clicked.connect(self.acquireShort)
        self.embedWidget.acquireLoad.clicked.connect(self.acquireLoad)

        self.embedWidget.reembedButton.clicked.connect(self.reembed)

        
        self.embedWidget.addPlug.clicked.connect(self.add_Plug)
        self.embedWidget.importPlug.clicked.connect(self.import_Plug)

        
        self.embedWidget.plugList.currentIndexChanged.connect(self.embedUpdatePlug)
        
        self.embedWidget.reverseCheckBox.toggled.connect(self.embedUpdateTab)
        
        self.parentTab.clear()


        #self.parentTab.addTab(self.embeddingTab, "Embedding Main")
        self.embedUpdateTab()

    def embedUpdatePlug(self, idx):
        print("idx : ", idx)
        plug = None
        try:
            plug = self.embedWidget.plugList.itemData(idx)
        except:
            print("No plug found. Please add a plug")
        #self.embeddedSample.getPlugParams(plugFile)
        #print(self.embeddedSample.plugNextDelay)

        

        if plug is not None:
            self.embeddedSample.setPlug(plug)
            self.embedWidget.dnext12_36.setText(str(plug.plugNextDelay["12-36"]))
            self.embedWidget.dnext45_12.setText(str(plug.plugNextDelay["45-12"]))
            self.embedWidget.dnext12_78.setText(str(plug.plugNextDelay["12-78"]))
            self.embedWidget.dnext45_36.setText(str(plug.plugNextDelay["45-36"]))
            self.embedWidget.dnext36_78.setText(str(plug.plugNextDelay["36-78"]))
            self.embedWidget.dnext45_78.setText(str(plug.plugNextDelay["45-78"]))
            

    def importOpen(self):
        self.embeddedSample.embeddedOpen = self.embedImportSNP()
        self.embedUpdateTab()

    def importShort(self):
        self.embeddedSample.embeddedShort = self.embedImportSNP()
        self.embedUpdateTab()
        
    def importLoad(self):
        print("Import LOAD")

        self.embeddedSample.embeddedLoad = self.embedImportSNP()
        self.embedUpdateTab()


    def acquireOpen(self):
        
        try:
            self.embeddedSample.embeddedOpen = self.comm.aquireInterface()
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please Connect to VNA")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()
        self.embedUpdateTab()

    def acquireShort(self):
        try:
            self.embeddedSample.embeddedShort = self.comm.aquireInterface()
        except Exception:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please Connect to VNA ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()
        self.embedUpdateTab()
        
    def acquireLoad(self):
        try:    
            self.embeddedSample.embeddedLoad = self.comm.aquireInterface()
            self.embedUpdateTab()

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please Connect to VNA ")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setFixedSize(msg.sizeHint())
            msg.exec_()
            print(e)
        
    def reembed(self):
       
        plug = self.embeddedSample.plug

        cat = "6A" if  self.embedWidget.embedCat6.isChecked() else "5"

        #self.embeddedSample.getPlugParams(plugFile)

        self.embeddedSample.k1 = self.embedWidget.SJ_124578_LineEdit.text()
        self.embeddedSample.k2 = self.embedWidget.sJ36LineEdit.text()
        self.embeddedSample.k3 = self.embedWidget.thruCalibLineEdit.text()

        #print(self.embeddedSample.k1)

        if self.embedtestType == "Reverse":
            #print(self.embeddedSample.embeddedOpen)
            if self.embeddedSample.embeddedOpen.isspace() or self.embeddedSample.embeddedShort.isspace() or self.embeddedSample.embeddedLoad.isspace():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Make sure that you have selected an open, short and load sample")
                msg.setWindowTitle("Reverse file missing")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setFixedSize(msg.sizeHint())
                msg.exec_()                
            else:
                self.embeddedSample.getJackVectorReverse(self.embeddedSample.embeddedOpen, self.embeddedSample.embeddedShort, self.embeddedSample.embeddedLoad)
                self.embeddedSample.reembed(cat)
                self.embedUpdateTab()

        else:
            if self.embeddedSample.embeddedLoad.isspace():
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Make sure that you have selected a load sample")
                msg.setWindowTitle("Forward file missing")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setFixedSize(msg.sizeHint())
                msg.exec_()
            else:
                self.embeddedSample.getJackVector(self.embeddedSample.embeddedLoad)
                self.embeddedSample.reembed(cat)
                self.embedUpdateTab()
       

    def embedImportSNP(self):
        print("IMPORTING EMBED SNP")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            return file

    def updatePlugList(self):
        print("updatePlugList HERE !")
        
        self.embedWidget.plugList.clear()

        if self.project is not None:
            for m in self.project.measurements:
                if m.__repr__() is "Plug":
                    print("M : ", m.name)
                    if m.calculated:
                        self.embedWidget.plugList.addItem(m.name, m)
                        print(m.name)

        if self.embeddedSample.plug is not None:
            idx = self.embedWidget.plugList.findData(self.embeddedSample.plug)
            self.embedWidget.plugList.setCurrentIndex(idx)


    def embedUpdateTab(self):
        if self.embeddedSample.cat == "6" or self.embeddedSample.cat == "6A" or self.embeddedSample.cat == "8":
            self.embedWidget.embedCat6.setDown(True)
        else:
            self.embedWidget.embedCat5.setDown(True)
    

        self.embedWidget.openFileName.setText(self.embeddedSample.embeddedOpen)
        self.embedWidget.shortFileName.setText(self.embeddedSample.embeddedShort)
        self.embedWidget.loadFileName.setText(self.embeddedSample.embeddedLoad)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.embedWidget.openFileName.setFont(font)
        self.embedWidget.shortFileName.setFont(font)
        self.embedWidget.loadFileName.setFont(font)

        self.updatePlugList()        

        self.parentTab.clear()

        self.parentTab.addTab(self.embeddingTab, "Embedding Main")

        embededParams = self.embeddedSample.getParameters()
        #print(embededParams)

        if bool(self.embeddedSample.reembeded):

            self.embeded_tab_list = []

            for key in embededParams.keys():
                self.new_Embededtab = QtWidgets.QWidget()
                self.embeded_tab_list.append(self.new_Embededtab)
                self.parentTab.addTab(self.new_Embededtab, key)
                
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

        self.embedWidget.SJ_124578_LineEdit.setText(str(self.embeddedSample.k1))
        self.embedWidget.sJ36LineEdit.setText(str(self.embeddedSample.k2))
        self.embedWidget.thruCalibLineEdit.setText(str(self.embeddedSample.k3))



    def add_Plug(self, t):
        self.proc_addPlug.emit()


    def import_Plug(self):
        self.proc_importPlug.emit()

    '''def addPlugDialog(self):

        form = PlugWidget.AddPlug()  # We set the  form to be our ExampleApp (design)

        #self.embedPlotUpdate()    '''     

    def embedPlotUpdate(self, activeParameter):
        sample = self.embeddedSample
        limit = None

        if sample.standard is not None:
            if activeParameter == "36-45":
                limit = sample.standard.limits["Mat. Next 1,4"].getArray()
            else:
                limit = sample.standard.limits["Mat. Next"].getArray()

        self.embedPlot(activeParameter, limit=limit)

    def embedPlot(self, activeParameter, limit):
        
        embededParams = self.embeddedSample.getParameters()

        if activeParameter != "Embedding Main":
            self.graphicsView.figure.clear()

            if activeParameter not in embededParams.keys():
                return
            
            ax=self.graphicsView.figure.add_subplot(111)
             
            color=iter(cm.rainbow(np.linspace(0, 1, len(embededParams[activeParameter]))))
            for case in embededParams[activeParameter]:
                c = next(color)
                reembedingNum = int(case.replace("case", ""))
                ax.semilogx(self.embeddedSample.freq, self.embeddedSample.reembeded[reembedingNum], label=case, c = c)

            if limit:
                ax.semilogx(*zip(*limit), label = "Limit") 
            ax.legend(loc='upper left', ncol =  2 )
 
            #self.figure.tight_layout()

            ax.grid(which="both")
            ax.set_xlabel('Freq (MHz)')
            ax.set_ylabel('dB')
            ax.set_title(activeParameter)
            self.graphicsView.draw()
        else:
            self.graphicsView.figure.clear()
            self.graphicsView.draw()