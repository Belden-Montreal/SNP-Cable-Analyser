from widgets.tab_widget import TabWidget
from widgets import plug_widget_ui
from widgets.cnext_tab import CNEXTTab
from PyQt5 import QtWidgets
from parameters.type import ParameterType

class PlugWidget(TabWidget, plug_widget_ui.Ui_Form):
    def __init__(self, plugNode, vnaManager):
        super(PlugWidget, self).__init__(self)
        self._vna = vnaManager
        self._vna.connection.connect(lambda: self.connect())
        self._node = plugNode
        self._plug = plugNode.getObject()
        self._loadName = None
        self._shortName = None
        self._openName = None
        self._dfOpenName = None
        self._dfShortName = None
        self.dfOpenImport.clicked.connect(lambda: self.getDfOpen())
        self.dfOpenAcquire.clicked.connect(lambda: self.getVnaDfOpen())
        self.dfShortImport.clicked.connect(lambda: self.getDfShort())
        self.dfShortAcquire.clicked.connect(lambda: self.getVnaDfShort())
        self.importOpen.clicked.connect(lambda: self.getOpen())
        self.acquireOpen.clicked.connect(lambda: self.getVnaOpen())
        self.importShort.clicked.connect(lambda: self.getShort())
        self.acquireShort.clicked.connect(lambda: self.getVnaShort())
        self.importLoad.clicked.connect(lambda: self.getLoad())
        self.acquireLoad.clicked.connect(lambda: self.getVnaLoad())
        self.recalcButton.clicked.connect(lambda: self.calculate())
        self._pairTabs = dict()
        self.createTabs()
        self.connect()
        self.updateWidget()

    def connect(self):
        if self._vna.connected():
            self.dfOpenAcquire.setEnabled(True)
            self.dfShortAcquire.setEnabled(True)
            self.acquireOpen.setEnabled(True)
            self.acquireShort.setEnabled(True)
            self.acquireLoad.setEnabled(True)
        else:
            self.dfOpenAcquire.setEnabled(False)
            self.dfShortAcquire.setEnabled(False)
            self.acquireOpen.setEnabled(False)
            self.acquireShort.setEnabled(False)
            self.acquireLoad.setEnabled(False)

    def getVnaDfOpen(self):
        fileName = self._vna.acquire()
        self._dfOpenName = fileName
        self.dfOpenFileName.setText(fileName)

    def getVnaDfShort(self):
        fileName = self._vna.acquire()
        self._dfShortName = fileName
        self.dfShortFileName.setText(fileName)

    def getVnaOpen(self):
        fileName = self._vna.acquire()
        self._openName = fileName
        self.openFileName.setText(fileName)

    def getVnaShort(self):
        fileName = self._vna.acquire()
        self._shortName = fileName
        self.shortFileName.setText(fileName)

    def getVnaLoad(self):
        fileName = self._vna.acquire()
        self._loadName = fileName
        self.loadFileName.setText(fileName)

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
        # try:
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
            self._node.updateChildren()
        else:
            error = QtWidgets.QErrorMessage(self)
            error.showMessage("Please select all the required files", "Missing_Files")
            error.exec_()
        # except Exception as e:
        #     error = QtWidgets.QErrorMessage(self)
        #     error.showMessage(("Please select valid s8p files. \n{}").format(str(e)), "Invalid_Files")
        #     error.exec_()

    def updateWidget(self):
        if self._plug.dfOpen():
            self._dfOpenName = self._plug.dfOpen().getFileName()
            self.dfOpenFileName.setText(self._plug._dfOpenDelay.getName())
        if self._plug.dfShort():
            self._dfShortName = self._plug.dfShort().getFileName()
            self.dfShortFileName.setText(self._plug._dfShortDelay.getName())
        if self._plug.openSample():
            self._openName = self._plug.openSample().getFileName()
            self.openFileName.setText(self._plug._openDelay.getName())
        if self._plug.shortSample():
            self._shortName = self._plug.shortSample().getFileName()
            self.shortFileName.setText(self._plug._shortDelay.getName())
        if self._plug.loadSample():
            self._loadName = self._plug.loadSample().getFileName()
            self.loadFileName.setText(self._plug._loadSample.getName())
        self.tabWidget.clear()
        self.tabWidget.addTab(self.mainTab, "main")
        for name, tab in self._pairTabs.items():
            self.tabWidget.addTab(tab, name)

    def createTabs(self):
        cnext = self._plug.getPlugNext()
        if cnext:
            series = cnext.getDataSeries()
            for serie in series:
                tab = CNEXTTab(serie, cnext)
                self._pairTabs[serie.getName()] = tab
