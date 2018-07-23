from widgets.tab_widget import TabWidget
from widgets import plug_widget_ui
from widgets.cnext_tab import CNEXTTab
from PyQt5 import QtWidgets

class PlugWidget(TabWidget, plug_widget_ui.Ui_Form):
    def __init__(self, plugNode):
        super(PlugWidget, self).__init__(self)
        self._node = plugNode
        self._plug = plugNode.getObject()
        self._loadName = None
        self._shortName = None
        self._openName = None
        self._dfOpenName = None
        self._dfShortName = None
        self.dfOpenImport.clicked.connect(lambda: self.getDfOpen())
        self.dfShortImport.clicked.connect(lambda: self.getDfShort())
        self.importOpen.clicked.connect(lambda: self.getOpen())
        self.importShort.clicked.connect(lambda: self.getShort())
        self.importLoad.clicked.connect(lambda: self.getLoad())
        self.recalcButton.clicked.connect(lambda: self.calculate())
        self._pairTabs = dict()
        self.createTabs()
        self.updateWidget()

    def getDfOpen(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Direct Fixture open file", "", "sNp Files (*.s*p)")
        self._dfOpenName = fileName
        self.dfOpenFileName.setText(fileName)

    def getDfShort(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Direct Fixture short file", "", "sNp Files (*.s*p)")
        self._dfShortName = fileName
        self.dfShortFileName.setText(fileName)

    def getOpen(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select open file", "", "sNp Files (*.s*p)")
        self._openName = fileName
        self.openFileName.setText(fileName)

    def getShort(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select short file", "", "sNp Files (*.s*p)")
        self._shortName = fileName
        self.shortFileName.setText(fileName)

    def getLoad(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select load file", "", "sNp Files (*.s*p)")
        self._loadName = fileName
        self.loadFileName.setText(fileName)

    def calculate(self):
        try:
            k1 = float(self.SJ_124578_LineEdit.text())
            k2 = float(self.sJ36LineEdit.text())
            k3 = float(self.thruCalibLineEdit.text())
            if self._dfOpenName and self._dfShortName and self._openName and self._shortName and self._loadName:
                
                self._plug.setConstants(k1, k2, k3)
                self._plug.importDfOpen(self._dfOpenName)
                self._plug.importDfShort(self._dfShortName)
                self._plug.importOpen(self._openName)
                self._plug.importShort(self._shortName)
                self._plug.importLoad(self._loadName)
                self.createTabs()
                self.updateWidget()
                self._node.addChildren([self._plug.dfOpen(), self._plug.dfShort(), self._plug.openSample(), self._plug.shortSample(), self._plug.loadSample()])
            else:
                error = QtWidgets.QErrorMessage(self)
                error.showMessage("Please select all the required files", "Missing_Files")
                error.exec_()
        except Exception as e:
            error = QtWidgets.QErrorMessage(self)
            error.showMessage(("Please select valid s8p files. \n{}").format(str(e)), "Invalid_Files")
            error.exec_()

    def updateWidget(self):
        if self._plug._dfOpenDelay:
            self.dfOpenFileName.setText(self._plug._dfOpenDelay.getName())
        if self._plug._dfShortDelay:
            self.dfShortFileName.setText(self._plug._dfShortDelay.getName())
        if self._plug._openDelay:
            self.openFileName.setText(self._plug._openDelay.getName())
        if self._plug._shortDelay:
            self.shortFileName.setText(self._plug._shortDelay.getName())
        if self._plug._loadSample:
            self.loadFileName.setText(self._plug._loadSample.getName())
        self.tabWidget.clear()
        self.tabWidget.addTab(self.mainTab, "main")
        for name, tab in self._pairTabs.items():
            self.tabWidget.addTab(tab, name)

    def createTabs(self):
        sample = self._plug._loadSample
        if sample:
            cnext = sample.getParameters()["CNEXT"]
            for port, (name,_) in cnext.getPorts().items():
                tab = CNEXTTab(name, cnext.getFrequencies(), cnext.getParameter()[port])
                self._pairTabs[name] = tab