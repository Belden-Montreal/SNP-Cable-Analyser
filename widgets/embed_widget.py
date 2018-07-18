from PyQt5 import QtWidgets
from widgets.tab_widget import TabWidget
from widgets.case_tab import CaseTab
from widgets import embed_widget_ui
from canvas import Canvas
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter

class EmbedWidget(TabWidget, embed_widget_ui.Ui_Form):
    def __init__(self, embedNode):
        super(EmbedWidget, self).__init__(self)
        self.reverseCheckBox.toggled.connect(lambda: self.reverse())
        self.categoryGroup = QtWidgets.QButtonGroup(self)
        self.categoryGroup.addButton(self.embedCat5)
        self.categoryGroup.addButton(self.embedCat6)
        self.categoryGroup.buttonClicked.connect(lambda: self.changeCategory())
        self.reembedButton.clicked.connect(lambda: self.reembed())
        self.importLoad.clicked.connect(lambda: self.getLoadFile())
        self.importPlug.clicked.connect(lambda: self.getPlug())
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
        self._k1, self._k2, self._k3 = None, None, None
        self.updateWidget()

    def updateWidget(self):
        side = self.getSide()
        sample = self._embedding.load()[side]
        if sample:
            self.loadFileName.setText(sample.getName())
        else:
            self.loadFileName.setText("\"\"")
        if len(self._embedding.reverse()) == 2:
            self.openFileName.setText(self._embedding.reverse()[0])
            self.shortFileName.setText(self._embedding.reverse()[1])
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

    def createTabs(self, side):
        sample = self._embedding.load()[side]
        if sample:
            cases = sample.getParameters()["Case"]
            for port, (name,_) in cases.getPorts().items():
                tab = CaseTab(name, cases.getFrequencies(), cases.getParameter()[port], self)
                self._pairTabs[side][name] = tab

    def reverse(self):
        self._isReverse = not self._isReverse
        self.openLabel.setEnabled(self._isReverse)
        self.acquireOpen.setEnabled(self._isReverse)
        self.importOpen.setEnabled(self._isReverse)
        self.openFileName.setEnabled(self._isReverse)
        self.shortLabel.setEnabled(self._isReverse)
        self.acquireShort.setEnabled(self._isReverse)
        self.importShort.setEnabled(self._isReverse)
        self.shortFileName.setEnabled(self._isReverse)
        self.updateWidget()

    def changeCategory(self):
        cat = self.categoryGroup.checkedButton().text()
        if cat == "Cat 5":
            self._cat = "CAT5e"
        else:
            self._cat = "CAT6"
        self.reembed()

    def getLoadFile(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select load file", "", "sNp Files (*.s*p)")
        self._loadFile = fileName
        self.reembed()

    def getPlug(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select plug file", "", "Belden Network Analyzer Project files (*.bnap)")
        plug = self._embedding.importPlug(fileName)
        self.plugLabel.setText(plug.getName())
        self.reembed()

    def reembed(self):
        if self._loadFile:
            if self._isReverse:
                pass #TODO: reverse Reembedding
            else:
                self.checkConstants()
                load = self._embedding.importLoad(self._loadFile, "Forward", self._cat)
                self.loadFileName.setText(load.getName())
                self._node.addChildren([load], self._embedding.plug(), "Forward")
            self.createTabs(self.getSide())
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