from PyQt5 import QtWidgets
from snpanalyzer.gui.widget.tab_widget import TabWidget
from snpanalyzer.gui.widget.case_tab import CaseTab
from snpanalyzer.gui.ui import embed_widget_ui
from snpanalyzer.parameters.type import ParameterType
from snpanalyzer.gui.widget.canvas import Canvas
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from snpanalyzer.gui.dialog.vna_test import VNATestDialog

class EmbedWidget(TabWidget, embed_widget_ui.Ui_Form):
    def __init__(self, embedNode, vnaManager):
        super(EmbedWidget, self).__init__(self)
        self._vna = vnaManager
        self._vna.connection.connect(lambda: self.connect())
        self.reverseCheckBox.toggled.connect(lambda: self.reverse())
        self.categoryGroup = QtWidgets.QButtonGroup(self)
        self.categoryGroup.addButton(self.embedCat5)
        self.categoryGroup.addButton(self.embedCat6)
        self.categoryGroup.buttonClicked.connect(lambda: self.changeCategory())
        self.reembedButton.clicked.connect(lambda: self.reembed())
        self.importLoad.clicked.connect(lambda: self.getLoadFile())
        self.importPlug.clicked.connect(lambda: self.getPlug())
        self.importOpen.clicked.connect(lambda: self.getOpen())
        self.importShort.clicked.connect(lambda: self.getShort())
        self.acquireLoad.clicked.connect(lambda: self.getVnaLoad())
        self.acquireOpen.clicked.connect(lambda: self.getVnaOpen())
        self.acquireShort.clicked.connect(lambda: self.getVnaShort())
        self._isReverse = False
        self._node = embedNode
        self._embedding = embedNode.getObject()
        self._cat = "Cat 6/6A"
        self._pairTabs = dict()
        self._pairTabs["Forward"] = dict()
        self._pairTabs["Reverse"] = dict()
        self.createTabs("Forward")
        self.createTabs("Reverse")
        self.tabWidget.setTabText(0, "main")
        self._loadFile = None
        self._openFile = None
        self._shortFile = None
        self._k1, self._k2, self._k3 = None, None, None
        self.connect()
        self._isReverse = True
        self.reverse()

    def connect(self):
        if self._vna.connected():
            self.acquireLoad.setEnabled(True)
            self.acquireOpen.setEnabled(True and self._isReverse)
            self.acquireShort.setEnabled(True and self._isReverse)
        else:
            self.acquireLoad.setEnabled(False)
            self.acquireOpen.setEnabled(False)
            self.acquireShort.setEnabled(False)

    def updateWidget(self):
        side = self.getSide()
        sample = self._embedding.load()[side]
        if sample:
            self.loadFileName.setText(sample.getName())
            self._loadFile = sample.getFileName()
        else:
            self.loadFileName.setText("\"\"")
            self._loadFile = None
        if side == "Reverse":
            if self._embedding.openSample():
                self._openFile = self._embedding.openSample().getFileName()
                self.openFileName.setText(self._embedding.openSample().getName())
            if self._embedding.shortSample():
                self._shortFile = self._embedding.shortSample().getFileName()
                self.shortFileName.setText(self._embedding.shortSample().getName())
        else:
            self.openFileName.setText("\"\"")
            self.shortFileName.setText("\"\"")
        if self._embedding.plug():
            plug = self._embedding.plug()
            self.plugLabel.setText(plug.getName())
            self._k1, self._k2, self._k3 = plug.getConstants()
            self.SJ_124578_LineEdit.setText(str(self._k1))
            self.sJ36LineEdit.setText(str(self._k2))
            self.thruCalibLineEdit.setText(str(self._k3))
        self.tabWidget.clear()
        self.tabWidget.addTab(self.mainTab, "main")
        for name, tab in self._pairTabs[side].items():
            self.tabWidget.addTab(tab, name)

        if self._vna.connected():
            self.acquireLoad.setEnabled(True)
            self.acquireOpen.setEnabled(True and self._isReverse)
            self.acquireShort.setEnabled(True and self._isReverse)
        else:
            self.acquireLoad.setEnabled(False)
            self.acquireOpen.setEnabled(False)
            self.acquireShort.setEnabled(False)

    def createTabs(self, side):
        sample = self._embedding.load()[side]
        if sample:
            if side == "Forward":
                cases = sample.getParameters()[ParameterType.CASE]
            else:
                cases = sample.getParameters()[ParameterType.RCASE]
            for serie in cases.getDataSeries():
                if sample.getStandard():
                    limit = sample.getStandard().limits["NEXT"]
                else:
                    limit = None
                tab = CaseTab(serie, cases, self, limit)
                self._pairTabs[side][serie.getName()] = tab

    def reverse(self):
        self._isReverse = not self._isReverse
        self.openLabel.setEnabled(self._isReverse)
        self.acquireOpen.setEnabled(self._isReverse and self._vna.connected())
        self.importOpen.setEnabled(self._isReverse)
        self.openFileName.setEnabled(self._isReverse)
        self.shortLabel.setEnabled(self._isReverse)
        self.acquireShort.setEnabled(self._isReverse and self._vna.connected())
        self.importShort.setEnabled(self._isReverse)
        self.shortFileName.setEnabled(self._isReverse)
        self.updateWidget()

    def changeCategory(self):
        cat = self.categoryGroup.checkedButton().text()
        if cat == "Cat 5":
            self._cat = "CAT5e"
        else:
            self._cat = "CAT6"

    def getLoadFile(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select load file", "", "sNp Files (*.s*p)")
        if fileName:
            self._loadFile = fileName
            self.loadFileName.setText(self._loadFile)

    def getPlug(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select plug file", "", " (*.xml)")
        if fileName:
            plug = self._embedding.importPlug(fileName)
            self.plugLabel.setText(plug.getName())
            self._k1, self._k2, self._k3 = plug.getConstants()
            self.SJ_124578_LineEdit.setText(str(self._k1))
            self.sJ36LineEdit.setText(str(self._k2))
            self.thruCalibLineEdit.setText(str(self._k3))
            self._node.updateChildren()

    def getOpen(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select open file", "", "sNp Files (*.s*p)")
        if fileName:
            self._openFile = fileName
            self.openFileName.setText(self._openFile)

    def getShort(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select short file", "", "sNp Files (*.s*p)")
        if fileName:
            self._shortFile = fileName
            self.shortFileName.setText(self._shortFile)

    def getVnaLoad(self):
        try:
            vnaDialog = VNATestDialog()
            vnaDialog.exec_()
            name = vnaDialog.getSampleName()
            ports = vnaDialog.getPorts()
            fileName = self._vnaManager.acquire(name, ports, vnaDialog.getVNACOnfiguration())

            if fileName:
                self._loadFile = fileName
                self.loadFileName.setText(self._loadFile)
        except Exception as e:
            print(e)  


    def getVnaOpen(self):

        try:
            vnaDialog = VNATestDialog()
            vnaDialog.exec_()
            name = vnaDialog.getSampleName()
            ports = vnaDialog.getPorts()
            fileName = self._vnaManager.acquire(name, ports, vnaDialog.getVNACOnfiguration())

            if fileName:
                self._openFile = fileName
                self.openFileName.setText(self._openFile)
        except Exception as e:
            print(e)  


    
    def getVnaShort(self):
        fileName = self._vna.acquire()
    
        try:
            vnaDialog = VNATestDialog()
            vnaDialog.exec_()
            name = vnaDialog.getSampleName()
            ports = vnaDialog.getPorts()
            fileName = self._vnaManager.acquire(name, ports, vnaDialog.getVNACOnfiguration())

            if fileName:
                self._shortFile = fileName
                self.shortFileName.setText(self._shortFile)
        except Exception as e:
            print(e)    



    def reembed(self):
        if self._isReverse:
            side = "Reverse"
            if self._openFile:
                openFile = self._embedding.importOpen(self._openFile)
                self.openFileName.setText(openFile.getName())
            if self._shortFile:
                shortFile = self._embedding.importShort(self._shortFile)
                self.shortFileName.setText(shortFile.getName())
        else:
            side = "Forward"
        if self._loadFile:
            self.checkConstants()
            load = self._embedding.importLoad(self._loadFile, side, self._cat)
            self.loadFileName.setText(load.getName())
            self.createTabs(self.getSide())
        self._node.updateChildren()
        self.updateWidget()

    def checkConstants(self):
        k1 = float(self.SJ_124578_LineEdit.text())
        k2 = float(self.sJ36LineEdit.text())
        k3 = float(self.thruCalibLineEdit.text())
        if not (k1 == self._k1 and k2 == self._k2 and k3 == self._k3):
            self._embedding.plug().setConstants(k1, k2, k3)
            self._embedding.plug().recalculate()

    def getSide(self):
        if self._isReverse:
            return "Reverse"
        else:
            return "Forward"